declare type OptionCommon = Record<string, any>;
export declare type Option = OptionCommon & {
    created?: boolean;
};
export declare type OptionGroup = OptionCommon;
export declare type OptionType = Option | OptionGroup;
export declare type OptionItemProps = {
    item: any;
    index: number;
    disabled: boolean;
};
export declare type SelectStates = {
    inputValue: string;
    cachedOptions: Option[];
    createdOptions: Option[];
    hoveringIndex: number;
    inputHovering: boolean;
    selectionWidth: number;
    calculatorWidth: number;
    collapseItemWidth: number;
    previousQuery: string | null;
    previousValue: unknown;
    selectedLabel: string;
    menuVisibleOnFocus: boolean;
    isBeforeHide: boolean;
};
export {};
