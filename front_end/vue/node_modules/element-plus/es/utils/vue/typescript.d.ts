import type { AppContext, EmitsOptions, Plugin, SetupContext } from 'vue';
export declare type SFCWithInstall<T> = T & Plugin;
export declare type SFCInstallWithContext<T> = SFCWithInstall<T> & {
    _context: AppContext | null;
};
export declare type EmitFn<E extends EmitsOptions> = SetupContext<E>['emit'];
