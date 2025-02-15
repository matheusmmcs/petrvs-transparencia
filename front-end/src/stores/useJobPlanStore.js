// stores/useJobPlanStore.js
import { PlansService } from '@/service/PlansService';
import { defineStore } from 'pinia';

export const useJobPlanStore = defineStore('jobPlanStore', {
    state: () => ({
        isPlansLoaded: false,
        plans: null,
        filteredPlans: null // Planos filtrados pela tabela
    }),
    actions: {
        async fetchPlans(dtIni, dfFim) {
            this.isPlansLoaded = false;
            try {
                this.plans = await PlansService.getPlans(dtIni, dfFim);
                this.filteredPlans = this.plans;
            } catch (error) {
                console.error('Erro ao buscar planos:', error);
            } finally {
                this.isPlansLoaded = true;
            }
        },
        clearPlans() {
            this.plans = null;
            this.filteredPlans = null;
            this.isPlansLoaded = true;
        },
        setFilteredPlans(filtered) {
            this.filteredPlans = filtered;
        }
    }
});
