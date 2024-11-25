<script setup lang="ts">
import {ref, computed, onMounted, reactive} from 'vue'
import {nanoid} from 'nanoid'
import axios from "axios";

const pageSize = 10;   // 每页显示的项数
const currentPage = ref(1); // 当前页码
const items = ref([]); // 存储所有卡片数据
const totalItems = ref(0); // 总项数

// 计算属性：获取当前页显示的卡片
const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return items.value.slice(start, start + pageSize);
});

// 处理页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage;
  console.log(`Current page: ${currentPage.value}`);
};

//组件挂载完成后请求历史记录
onMounted(async () => {
      try {
          const response = await axios.get('/api/history');
          // console.log(response.data)
          response.data.forEach(item => {
          let descriment;
          if(item.model.length == 1){
            descriment="单模型预测: "
          }
          else{
            descriment="多模型预测叠加: "
          }
          for(let i=0;i<item.model.length;i++){
            if(i!=0) descriment+=","
            descriment+=item.model[i]
          }
          const now = reactive([])
          for(let i=0;i<item.original.length;i++){
            now.push({
              id: nanoid(),
              original: item.original[i],
              predict: item.predict[i],
              filename: item.filename[i],
              datetime : item.datetime,
              model : descriment
            })
          }
          items.value.push(now)
    });
      } catch (error) {
          console.error('Failed to fetch workspace:', error);
      }
    totalItems.value = items.value.length;
    console.log(items.value)
});

</script>

<template>
  <div class="example-pagination-block">
    <div class="card-container">
        <el-card
        v-for="(items,index) in paginatedItems"
        :key="index"
        style="flex: 1; margin: 10px;max-width: 900px"
      >
        <div style="padding: 10px;">
            <h4>时间: {{ items[0].datetime }} </h4>
            <p>文件: {{ items[0].filename }} </p>
            <p>{{ items[0].model }}</p>
          </div>
        <div v-for="item in items"
             :key="item.id"
            class="image-container" style="display: flex;margin-top: 20px"
        >

          <el-image
              style="margin-right: 30%;width: 200px;"
              :src="item.original"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[item.original]"
              fit="cover"
          />
          <el-image
              style="margin-right: 80px;width: 200px;"
              :src="item.predict"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[item.predict]"
              fit="cover"
          />

      </div>
        </el-card>
    </div>
    <el-pagination class="fenye"
      layout="prev, pager, next"
      :total="totalItems"
      :page-size="pageSize"
      :current-page="currentPage"
      @current-change="handlePageChange"
    />
  </div>
</template>
<style scoped>
  .example-pagination-block {
  margin: 20px;
}
  .fenye {
  display: flex;
  justify-content: center;
}
</style>