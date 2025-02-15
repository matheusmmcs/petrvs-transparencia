<script setup>
import PlansChart from '@/components/dashboard/pgd/PlansChart.vue';
import PlansFilter from '@/components/dashboard/pgd/PlansFilter.vue';
import PlansMonthlyTable from '@/components/dashboard/pgd/PlansMonthlyTable.vue';
</script>

<template>
    <div class="grid grid-cols-12 gap-8">
        <PlansFilter />
        <PlansChart />
        <div class="col-span-12 xl:col-span-12">
            <PlansMonthlyTable />
        </div>
    </div>
</template>
