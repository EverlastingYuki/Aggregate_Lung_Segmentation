import {defineStore} from 'pinia';
import {ref} from 'vue';

export const useAsideStore = defineStore("useAsideStore", () => {
    const selectedAsideFunction = ref('对比推理');
    const setFunction = (className: string) => {
        selectedAsideFunction.value = className;
    };
    return{
        selectedAsideFunction,
        setFunction
    }
})