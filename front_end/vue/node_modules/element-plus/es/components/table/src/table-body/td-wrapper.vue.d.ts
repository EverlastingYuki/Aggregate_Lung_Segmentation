declare const _default: __VLS_WithTemplateSlots<import("vue").DefineComponent<{
    colspan: {
        type: NumberConstructor;
        default: number;
    };
    rowspan: {
        type: NumberConstructor;
        default: number;
    };
}, {}, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, Record<string, any>, string, import("vue").VNodeProps & import("vue").AllowedComponentProps & import("vue").ComponentCustomProps, Readonly<import("vue").ExtractPropTypes<{
    colspan: {
        type: NumberConstructor;
        default: number;
    };
    rowspan: {
        type: NumberConstructor;
        default: number;
    };
}>>, {
    rowspan: number;
    colspan: number;
}>, {
    default?(_: {}): any;
}>;
export default _default;
declare type __VLS_WithTemplateSlots<T, S> = T & {
    new (): {
        $slots: S;
    };
};
