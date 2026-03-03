import React from "react";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface MetricBadgeProps {
    value: string;
    trend: "up" | "down" | "neutral";
    className?: string;
}

export function MetricBadge({ value, trend, className }: MetricBadgeProps) {
    const isUp = trend === "up";
    const isDown = trend === "down";

    return (
        <div className={cn(
            "flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold tracking-tight",
            isUp ? "bg-emerald-500/10 text-emerald-500" :
                isDown ? "bg-red-500/10 text-red-500" :
                    "bg-zinc-500/10 text-zinc-500",
            className
        )}>
            {isUp && <ArrowUpRight size={12} />}
            {isDown && <ArrowDownRight size={12} />}
            {value}
        </div>
    );
}
