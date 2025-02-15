<script setup>
import { useJobPlanStore } from '@/stores/useJobPlanStore';
import { FilterMatchMode, FilterOperator } from '@primevue/core/api';
import { storeToRefs } from 'pinia';
import { onBeforeMount, onMounted, reactive, ref, watch } from 'vue';

// Instancia o store
const store = useJobPlanStore();
const { plans, filteredPlans, isPlansLoaded } = storeToRefs(store);

// Aguarda a requisição antes de renderizar
const filters = ref(null);
const loading = ref(true);
const showModal = ref(false);
const userModal = ref(null);
const filteredData = ref([]); // Guarda os dados filtrados

// Atualiza os planos filtrados no Pinia
const atualizarDadosFiltrados = () => {
    store.setFilteredPlans(filteredData.value);
};

// Captura a filtragem do DataTable
const onFilter = (event) => {
    filteredData.value = event.filteredValue || [];
};

const statuses = reactive(['INCLUIDO', 'AGUARDANDO_ASSINATURA', 'ATIVO', 'CONCLUIDO']);
const modalidades = reactive(['Presencial', 'Teletrabalho (Parcial)', 'Teletrabalho (Integral)']);

function getSeverity(status) {
    switch (status) {
        case 'INCLUIDO':
            return 'danger';

        case 'CONCLUIDO':
            return 'success';

        case 'ATIVO':
            return 'info';

        case 'AGUARDANDO_ASSINATURA':
            return 'warn';

        case '':
            return null;
    }
}

onBeforeMount(() => {
    initFilters();
});

// Atualiza os dados filtrados na inicialização
onMounted(() => {
    atualizarDadosFiltrados();
});

function initFilters() {
    filters.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        plano_trabalho_data_inicio: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
        plano_trabalho_data_fim: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
        usuario_nome: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        modalidade_nome: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        plano_trabalho_status: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        unidade_sigla: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }] }
    };
}

function clearFilter() {
    initFilters();
}

function formatDate(value) {
    return value.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

function selectRow(data) {
    userModal.value = data;
    showModal.value = true;
}

watch(filteredData, atualizarDadosFiltrados, { deep: true });

watch(
    isPlansLoaded,
    () => {
        loading.value = !isPlansLoaded.value;
    },
    { deep: true }
);
</script>

<template>
    <div class="card">
        <div class="font-semibold text-xl mb-2">Planos de Trabalho</div>
        <div v-if="!loading" class="mb-4">
            <span class="text-muted-color mr-2">Total de</span>
            <span class="text-primary font-medium mr-2">{{ filteredPlans?.length || 0 }}</span>
            <span class="text-muted-color">planos.</span>
        </div>
        <DataTable
            :value="plans"
            dataKey="plano_trablho_id"
            :loading="loading"
            filterDisplay="menu"
            :filters="filters"
            v-model:filters="filters"
            @filter="onFilter"
            :globalFilterFields="['usuario_nome', 'unidade_nome', 'unidade_sigla', 'plano_trabalho_numero', 'modalidade_nome', 'plano_trabalho_status']"
            tableStyle="min-width: 50rem"
            :paginator="true"
            :rows="10"
            :rowsPerPageOptions="[5, 10, 20, 50]"
            paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
            currentPageReportTemplate="{first} até {last} de {totalRecords}"
            :rowHover="true"
            showGridlines
        >
            <template #header>
                <div class="flex justify-between">
                    <Button type="button" icon="pi pi-filter-slash" label="Limpar Filtros" outlined @click="clearFilter()" />
                    <IconField>
                        <InputIcon>
                            <i class="pi pi-search" />
                        </InputIcon>
                        <InputText v-model="filters['global'].value" placeholder="Filtrar" />
                    </IconField>
                </div>
            </template>
            <template #empty> Sem Planos de Trabalho encontrados. </template>
            <template #loading> Carregando Planos de Trabalho, aguarde. </template>
            <Column field="plano_trabalho_numero" sortable header="#"></Column>
            <Column header="Status" field="plano_trabalho_status" sortable :filterMenuStyle="{ width: '14rem' }">
                <template #body="{ data }">
                    <Tag :value="data.plano_trabalho_status" :severity="getSeverity(data.plano_trabalho_status)" />
                </template>
                <template #filter="{ filterModel }">
                    <Select v-model="filterModel.value" :options="statuses" placeholder="Selecione Uma" showClear>
                        <template #option="slotProps">
                            <Tag :value="slotProps.option" :severity="getSeverity(slotProps.option)" />
                        </template>
                    </Select>
                </template>
            </Column>
            <Column field="modalidade_nome" sortable header="Modalidade" style="min-width: 12rem">
                <template #body="{ data }">
                    {{ data.modalidade_nome }}
                </template>
                <template #filter="{ filterModel }">
                    <Select v-model="filterModel.value" :options="modalidades" placeholder="Selecione Uma" showClear>
                        <template #option="slotProps">
                            <Tag :value="slotProps.option" :severity="getSeverity(slotProps.option)" />
                        </template>
                    </Select>
                </template>
            </Column>
            <Column field="usuario_nome" sortable header="Servidor">
                <template #body="{ data }">
                    {{ data.usuario_nome }}
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" placeholder="Buscar por nome" />
                </template>
            </Column>
            <Column field="unidade_sigla" sortable header="Unidade">
                <template #body="{ data }">
                    {{ data.unidade_sigla }}
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" placeholder="Buscar por unidade" />
                </template>
            </Column>
            <Column field="plano_trabalho_data_inicio" header="Início" dataType="date" style="min-width: 10rem" filterField="plano_trabalho_data_inicio">
                <template #body="{ data }">
                    {{ formatDate(data.plano_trabalho_data_inicio) }}
                </template>
                <template #filter="{ filterModel }">
                    <DatePicker v-model="filterModel.value" dateFormat="dd/mm/yy" placeholder="dd/mm/yyyy" />
                </template>
            </Column>
            <!-- <Column field="plano_trabalho_data_fim" header="Término" dataType="date" style="min-width: 10rem" filterField="plano_trabalho_data_fim">
                <template #body="{ data }">
                    {{ formatDate(data.plano_trabalho_data_fim) }}
                </template>
                <template #filter="{ filterModel }">
                    <DatePicker v-model="filterModel.value" dateFormat="dd/mm/yy" placeholder="dd/mm/yyyy" />
                </template>
            </Column> -->

            <Column class="w-24 !text-center" header="Detalhes">
                <template #body="{ data }">
                    <Button icon="pi pi-search" @click="selectRow(data)" severity="secondary" rounded></Button>
                </template>
            </Column>
        </DataTable>

        <Dialog v-model:visible="showModal" maximizable modal header="Header" :style="{ width: '50rem' }" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
            <Accordion :value="['0', '1', '2']" multiple>
                <AccordionPanel value="0" v-if="userModal">
                    <AccordionHeader>Servidor</AccordionHeader>
                    <AccordionContent>
                        <div class="flex flex-col items-start justify-start gap-2">
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Nome:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.usuario_nome }} </span>
                            </div>
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">CPF (mascarado):</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.usuario_cpf_mascarado }} </span>
                            </div>
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">E-Mail:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.usuario_email_filtrado }} </span>
                            </div>
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Telefone:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.usuario_telefone }} </span>
                            </div>
                        </div>
                    </AccordionContent>
                </AccordionPanel>
                <AccordionPanel value="1">
                    <AccordionHeader>Plano de Trabalho</AccordionHeader>
                    <AccordionContent>
                        <div class="flex flex-col items-start justify-start gap-2">
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Número:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.plano_trabalho_numero }} </span>
                            </div>
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Status:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.plano_trabalho_status }} </span>
                            </div>
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Modalidade:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.modalidade_nome }} </span>
                            </div>
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Data de Início:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ formatDate(userModal.plano_trabalho_data_inicio) }} </span>
                            </div>
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Data de Término:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ formatDate(userModal.plano_trabalho_data_fim) }} </span>
                            </div>
                        </div>
                    </AccordionContent>
                </AccordionPanel>
                <AccordionPanel value="2">
                    <AccordionHeader>Unidade do Plano</AccordionHeader>
                    <AccordionContent>
                        <div class="flex flex-col items-start justify-start gap-2">
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Nome da Unidade:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.unidade_nome }} </span>
                            </div>
                            <div class="flex flex-row items-center justify-start gap-2 font-medium text-md">
                                <div class="">Sigla da Unidade:</div>
                                <span class="text-surface-500 dark:text-surface-400"> {{ userModal.unidade_sigla }} </span>
                            </div>
                        </div>
                    </AccordionContent>
                </AccordionPanel>
            </Accordion>
        </Dialog>
    </div>
</template>

<style scoped lang="scss">
:deep(.p-datatable-frozen-tbody) {
    font-weight: bold;
}

:deep(.p-datatable-scrollable .p-frozen-column) {
    font-weight: bold;
}
</style>
