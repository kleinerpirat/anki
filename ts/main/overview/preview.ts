// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

/* eslint
@typescript-eslint/no-explicit-any: "off",
 */

import * as tr from "@tslib/ftl";
import { localizedNumber } from "@tslib/i18n";
import type { Stats } from "@tslib/proto";
import {
    arc,
    cumsum,
    interpolate,
    pie,
    scaleLinear,
    schemeBlues,
    schemeGreens,
    schemeOranges,
    schemeReds,
    select,
    sum,
} from "d3";

import type { GraphBounds } from "../../graphs/graph-helpers";

type Count = [string, string, number];
export interface GraphData {
    label: string;
    counts: Count[];
    totalCards: string;
}

export interface TableData {
    [key: string]: {
        label: string;
        count: number;
        color: string;
    };
}

const barColours = [
    schemeBlues[5][2] /* new */,
    schemeReds[5][2] /* learn */,
    schemeOranges[5][2] /* relearn */,
    schemeGreens[5][2] /* young */,
    schemeGreens[5][3] /* mature */,
];

function countCards(data: Stats.GraphsResponse): Count[] {
    const countData = data.cardCounts!.excludingInactive!;

    const counts: Count[] = [
        ["new", tr.statisticsCountsNewCards(), countData.newCards],
        ["learn", tr.statisticsCountsLearningCards(), countData.learn],
        ["relearn", tr.statisticsCountsRelearningCards(), countData.relearn],
        ["young", tr.statisticsCountsYoungCards(), countData.young],
        ["mature", tr.statisticsCountsMatureCards(), countData.mature],
    ];

    return counts;
}

export function gatherData(data: Stats.GraphsResponse): GraphData {
    const counts = countCards(data);
    const totalCards = localizedNumber(sum(counts, (e) => e[2]));

    return {
        label: tr.statisticsPreviewTitle(),
        counts,
        totalCards,
    };
}

export interface SummedDatum {
    key: string;
    label: string;
    // count of this particular item
    count: number;
    // running total
    total: number;
}

export interface TableDatum {
    key: string;
    label: string;
    count: number;
    color: string;
}

export function renderPreview(
    svgElem: SVGElement,
    bounds: GraphBounds,
    sourceData: GraphData,
): TableData {
    const summed = cumsum(sourceData.counts, (d: Count) => d[2]);
    const data = Array.from(summed).map((n, idx) => {
        const count = sourceData.counts[idx];
        return {
            key: count[0],
            label: count[1],
            count: count[2],
            idx,
            total: n,
        } as SummedDatum;
    });
    // ensuring a non-zero range makes the percentages not break
    // in an empty collection
    const xMax = Math.max(1, summed.slice(-1)[0]);
    const x = scaleLinear().domain([0, xMax]);
    const svg = select(svgElem);
    const paths = svg.select(".counts");
    const pieData = pie()(sourceData.counts.map((d: Count) => d[2]));
    const radius = bounds.height / 2 - bounds.marginTop - bounds.marginBottom;
    const arcGen = arc().innerRadius(0).outerRadius(radius);
    const trans = svg.transition().duration(200) as any;

    paths
        .attr("transform", `translate(${radius},${radius + bounds.marginTop})`)
        .selectAll("path")
        .data(pieData)
        .join(
            (enter) =>
                enter
                    .append("path")
                    .attr("fill", (_d, idx) => {
                        return barColours[idx];
                    })
                    .attr("d", arcGen as any),
            function (update) {
                return update.call((d) =>
                    d.transition(trans).attrTween("d", (d) => {
                        const interpolator = interpolate(
                            { startAngle: 0, endAngle: 0 },
                            d,
                        );
                        return (t): string => arcGen(interpolator(t) as any) as string;
                    }),
                );
            },
        );

    x.range([bounds.marginLeft, bounds.width - bounds.marginRight]);

    return data.reduce(
        (obj: TableData, d: SummedDatum, idx: number) => ({
            ...obj,
            [d.key]: {
                label: d.label,
                count: d.count,
                color: barColours[idx],
            },
        }),
        {},
    );
}
