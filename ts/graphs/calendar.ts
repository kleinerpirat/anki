// Copyright: Ankitects Pty Ltd and contributors
// License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import { Stats } from "@tslib/proto";
import type { CountableTimeInterval } from "d3";
import { timeHour } from "d3";
import {
    timeDay,
    timeFriday,
    timeMonday,
    timeSaturday,
    timeSunday,
    timeYear,
} from "d3";

import { RevlogRange } from "./graph-helpers";

export interface GraphData {
    // indexed by day, where day is relative to today
    reviewCount: Map<number, number>;
    timeFunction: CountableTimeInterval;
    weekdayLabels: number[];
    rolloverHour: number;
}

interface DayDatum {
    day: number;
    count: number;
    // 0-51
    weekNumber: number;
    // 0-6
    weekDay: number;
    date: Date;
}

type WeekdayType = Stats.GraphPreferences.Weekday;
const Weekday = Stats.GraphPreferences.Weekday; /* enum */

export function gatherData(
    data: Stats.GraphsResponse,
    firstDayOfWeek: WeekdayType,
): GraphData {
    const reviewCount = new Map(
        Object.entries(data.reviews!.count).map(([k, v]) => {
            return [Number(k), v.learn + v.relearn + v.mature + v.filtered + v.young];
        }),
    );
    const timeFunction = timeFunctionForDay(firstDayOfWeek);
    const weekdayLabels: number[] = [];
    for (let i = 0; i < 7; i++) {
        weekdayLabels.push((firstDayOfWeek + i) % 7);
    }

    return {
        reviewCount,
        timeFunction,
        weekdayLabels,
        rolloverHour: data.rolloverHour,
    };
}

export function renderCalendar(
    sourceData: GraphData,
    targetYear: number,
    revlogRange: RevlogRange,
): { map: Map<number, DayDatum>; maxCount: number } {
    const now = new Date();

    // map of 0-365 -> day
    const dayMap: Map<number, DayDatum> = new Map();
    let maxCount = 0;
    for (const [day, count] of sourceData.reviewCount.entries()) {
        let date = timeDay.offset(now, day);
        // anki day does not necessarily roll over at midnight, we account for this when mapping onto calendar days
        date = timeHour.offset(date, -1 * sourceData.rolloverHour);
        if (count > maxCount) {
            maxCount = count;
        }
        if (date.getFullYear() != targetYear) {
            continue;
        }
        const weekNumber = sourceData.timeFunction.count(timeYear(date), date);
        const weekDay = timeDay.count(sourceData.timeFunction(date), date);
        const yearDay = timeDay.count(timeYear(date), date);
        dayMap.set(yearDay, { day, count, weekNumber, weekDay, date } as DayDatum);
    }

    const timestampMap: Map<number, DayDatum> = new Map();
    dayMap.forEach((entry) =>
        timestampMap.set(entry.date.getTime(), entry),
    );

    return { map: timestampMap, maxCount };
}

function timeFunctionForDay(firstDayOfWeek: WeekdayType): CountableTimeInterval {
    switch (firstDayOfWeek) {
        case Weekday.MONDAY:
            return timeMonday;
        case Weekday.FRIDAY:
            return timeFriday;
        case Weekday.SATURDAY:
            return timeSaturday;
        default:
            return timeSunday;
    }
}
