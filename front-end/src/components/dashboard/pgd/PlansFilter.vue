<script setup>
import { useJobPlanStore } from '@/stores/useJobPlanStore';
import { storeToRefs } from 'pinia';
import ProgressSpinner from 'primevue/progressspinner';
import { computed, onMounted, ref } from 'vue';

const store = useJobPlanStore();
const { filteredPlans } = storeToRefs(store);

const selectedMonthYear = ref(new Date());
const minDate = ref(new Date(2024, 10));
const isLoading = ref(false);

const getDatesRange = (d) => {
    const year = d.getFullYear();
    const month = d.getMonth();

    const startDate = new Date(year, month, 1);
    const endDate = new Date(year, month + 1, 1);

    const formattedStartDate = startDate.toISOString().split('T')[0];
    const formattedEndDate = endDate.toISOString().split('T')[0];

    return {
        formattedStartDate,
        formattedEndDate
    };
};

const handleDateChange = (newValue) => {
    if (newValue) {
        fetchPlans();
    }
};

const fetchPlans = async () => {
    isLoading.value = true;
    store.clearPlans();
    const { formattedStartDate, formattedEndDate } = getDatesRange(selectedMonthYear.value);
    await store.fetchPlans(formattedStartDate, formattedEndDate);
    isLoading.value = false;
};

const actualMonth = computed(() => {
    const d = selectedMonthYear.value;
    return `${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getFullYear()}`;
});

onMounted(() => {
    fetchPlans();
});
</script>

<template>
    <div class="col-span-12 lg:col-span-6 xl:col-span-6 flex">
        <div class="card mb-0 flex flex-col w-full min-h-[300px]">
            <div class="flex justify-start mb-4 gap-2 align-middle">
                <span class="font-bold text-xl">Mês de Referência:</span>
                <span class="text-primary text-xl">({{ actualMonth }})</span>
            </div>
            <div v-if="!isLoading" class="mb-4">
                <span class="text-muted-color mr-2">Total de</span>
                <span class="text-primary font-medium mr-2">{{ filteredPlans?.length || 0 }}</span>
                <span class="text-muted-color">planos.</span>
            </div>
            <DatePicker v-model="selectedMonthYear" inline view="month" dateFormat="mm/yy" :minDate="minDate" @update:modelValue="handleDateChange" />
            <!-- Animação de carregamento (spinner) com sobreposição -->
            <div v-if="isLoading" class="overlay flex justify-center items-center absolute inset-0 bg-white bg-opacity-50 z-10">
                <ProgressSpinner style="width: 50px; height: 50px" />
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Estilos para a sobreposição (overlay) */
.overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.6); /* Cor da sobreposição */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10; /* Garante que o overlay fique acima do calendário */
    border-radius: 8px; /* Opcional: arredondar os cantos da sobreposição */
}

.card {
    position: relative;
}
</style>
