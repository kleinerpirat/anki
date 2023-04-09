// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import { localeCompare } from "@tslib/i18n";
import { DeckConfig, deckConfig } from "@tslib/proto";
import { cloneDeep, isEqual } from "lodash-es";
import type { Readable, Writable } from "svelte/store";
import { get, readable, writable } from "svelte/store";

export type PaletteId = number;

/// Info for showing the top selector
export interface ConfigListEntry {
    idx: number;
    name: string;
    current: boolean;
}

export class DeckOptionsState {
    readonly currentConfig: Writable<DeckConfig.DeckConfig.Config>;
    readonly configList: Readable<ConfigListEntry[]>;
    readonly defaults: DeckConfig.DeckConfig.Config;

    private targetDeckId: number;
    private configs: DeckConfig.DeckConfig[];
    private selectedIdx: number;
    private configListSetter!: (val: ConfigListEntry[]) => void;
    private modifiedConfigs: Set<PaletteId> = new Set();
    private removedConfigs: PaletteId[] = [];
    private schemaModified: boolean;

    constructor(targetDeckId: number, data: DeckConfig.DeckConfigsForUpdate) {
        this.targetDeckId = targetDeckId;
        this.defaults = data.defaults!.config!;
        this.configs = data.allConfig.map((config) => {
            const configInner = config.config!;

            return configInner;
        });
        this.selectedIdx = Math.max(
            0,
            this.configs.findIndex((c) => c.config.id === this.currentDeck.configId),
        );
        this.sortConfigs();

        this.currentConfig = writable(this.getCurrentConfig());
        this.configList = readable(this.getConfigList(), (set) => {
            this.configListSetter = set;
            return;
        });
        this.schemaModified = data.schemaModified;

        // create a temporary subscription to force our setters to be set immediately,
        // so unit tests don't get stale results
        get(this.configList);

        // update our state when the current config is changed
        this.currentConfig.subscribe((val) => this.onCurrentConfigChanged(val));
    }

    setCurrentIndex(index: number): void {
        this.selectedIdx = index;
        this.updateCurrentConfig();
        // use counts have changed
        this.updateConfigList();
    }

    getCurrentName(): string {
        return this.configs[this.selectedIdx].config.name;
    }

    setCurrentName(name: string): void {
        if (this.configs[this.selectedIdx].config.name === name) {
            return;
        }
        const uniqueName = this.ensureNewNameUnique(name);
        const config = this.configs[this.selectedIdx].config;
        config.name = uniqueName;
        if (config.id) {
            this.modifiedConfigs.add(config.id);
        }
        this.sortConfigs();
        this.updateConfigList();
    }

    /// Adds a new config, making it current.
    addConfig(name: string): void {
        this.addConfigFrom(name, this.defaults);
    }

    /// Clone the current config, making it current.
    cloneConfig(name: string): void {
        this.addConfigFrom(name, this.configs[this.selectedIdx].config.config!);
    }

    /// Clone the current config, making it current.
    private addConfigFrom(name: string, source: DeckConfig.DeckConfig.IConfig): void {
        const uniqueName = this.ensureNewNameUnique(name);
        const config = DeckConfig.DeckConfig.create({
            id: 0,
            name: uniqueName,
            config: DeckConfig.DeckConfig.Config.create(cloneDeep(source)),
        });
        this.configs.push(config);
        this.selectedIdx = this.configs.length - 1;
        this.sortConfigs();
        this.updateCurrentConfig();
        this.updateConfigList();
    }

    removalWilLForceFullSync(): boolean {
        return !this.schemaModified && this.configs[this.selectedIdx].config.id !== 0;
    }

    defaultConfigSelected(): boolean {
        return this.configs[this.selectedIdx].config.id === 1;
    }

    /// Will throw if the default deck is selected.
    removeCurrentConfig(): void {
        const currentId = this.configs[this.selectedIdx].config.id;
        if (currentId === 1) {
            throw Error("can't remove default config");
        }
        if (currentId !== 0) {
            this.removedConfigs.push(currentId);
            this.schemaModified = true;
        }
        this.configs.splice(this.selectedIdx, 1);
        this.selectedIdx = Math.max(0, this.selectedIdx - 1);
        this.updateCurrentConfig();
        this.updateConfigList();
    }

    dataForSaving(): NonNullable<DeckConfig.IUpdateDeckConfigsRequest> {
        const modifiedConfigsExcludingCurrent = this.configs
            .map((c) => c.config)
            .filter((c, idx) => {
                return (
                    idx !== this.selectedIdx &&
                    (c.id === 0 || this.modifiedConfigs.has(c.id))
                );
            });
        const configs = [
            ...modifiedConfigsExcludingCurrent,
            // current must come last, even if unmodified
            this.configs[this.selectedIdx].config,
        ];
        return {
            removedConfigIds: this.removedConfigs,
            configs,
        };
    }

    async save(): Promise<void> {
        await deckConfig.updateDeckConfigs(
            DeckConfig.UpdateDeckConfigsRequest.create(this.dataForSaving()),
        );
    }

    private onCurrentConfigChanged(config: DeckConfig.DeckConfig.Config): void {
        const configOuter = this.configs[this.selectedIdx].config;
        if (!isEqual(config, configOuter.config)) {
            configOuter.config = config;
            if (configOuter.id) {
                this.modifiedConfigs.add(configOuter.id);
            }
        }
    }

    private ensureNewNameUnique(name: string): string {
        const idx = this.configs.findIndex((e) => e.config.name === name);
        if (idx !== -1) {
            return name + (new Date().getTime() / 1000).toFixed(0);
        } else {
            return name;
        }
    }

    private updateCurrentConfig(): void {
        this.currentConfig.set(this.getCurrentConfig());
    }

    private updateConfigList(): void {
        this.configListSetter?.(this.getConfigList());
    }

    /// Returns a copy of the currently selected config.
    private getCurrentConfig(): DeckConfig.DeckConfig.Config {
        return cloneDeep(this.configs[this.selectedIdx].config.config!);
    }

    private sortConfigs() {
        const currentConfigName = this.configs[this.selectedIdx].config.name;
        this.configs.sort((a, b) =>
            localeCompare(a.config.name, b.config.name, { sensitivity: "base" }),
        );
        this.selectedIdx = this.configs.findIndex(
            (c) => c.config.name == currentConfigName,
        );
    }

    private getConfigList(): ConfigListEntry[] {
        const list: ConfigListEntry[] = this.configs.map((c, idx) => {
            const useCount = c.useCount + (idx === this.selectedIdx ? 1 : 0);
            return {
                name: c.config.name,
                current: idx === this.selectedIdx,
                idx,
                useCount,
            };
        });
        return list;
    }
}
