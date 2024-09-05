<template>
  <el-container class="reference-example-container">
    <el-header>
      <div>Macro Photography IQA</div>
      <div>{{ userId }}</div>
    </el-header>
    <el-main class="main">
      <div class="content">
        <div class="demo-image__preview">
          <el-image
            class="demo-image"
            :src="getImageUrl(currentExample.image_id)"
            :preview-src-list="[getImageUrl(currentExample.image_id)]"
            :error="errorImageUrl"
          ></el-image>
        </div>
        <div class="text-container">
          <div class="rate">
            <strong>Recommended Rate:</strong> {{ getRateRange(currentExample.min_rate, currentExample.max_rate) }}
          </div>
          <div class="reason"><strong>Reason:</strong> {{ currentExample.reason }}</div>
          <div class="tag"><strong>Recommended Tag:</strong> {{ currentExample['recommended tag'] }}</div>
        </div>
      </div>
      <div class="buttons-pagination-container">
        <el-pagination
          class="pagination"
          background
          layout="prev, pager, next"
          :total="examples.length"
          :page-size="pageSize"
          @current-change="handlePageChange"
        ></el-pagination>
        <div class="button-container">
          <el-button type="primary" round @click="goback">Go back</el-button>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import exampleData from '@/assets/example.json';

export default {
  name: 'ReferenceExample',
  created() {
    this.userId = this.$route.params.id;
    this.batch = this.$route.params.batch;
    this.examples = exampleData.image_list;
  },
  data() {
    return {
      userId: null,
      batch: null,
      examples: [],
      errorImageUrl: require('@/assets/error.png'),
      currentPage: 1,
      pageSize: 1,
    };
  },
  computed: {
    currentExample() {
      const start = (this.currentPage - 1) * this.pageSize;
      return this.examples[start];
    }
  },
  methods: {
    getImageUrl(imageId) {
      return require(`@/components/examples/${imageId}.png`);
    },
    handlePageChange(page) {
      this.currentPage = page;
    },
    goback() {
      this.$router.push({ name: 'MainPage', params: { id: this.userId, batch: this.batch } });
    },
    getRateRange(minRate, maxRate) {
      const rateMap = {
        0: 'Bad',
        25: 'Poor',
        50: 'Fair',
        75: 'Good',
        100: 'Excellent'
      };
      const range = [];
      for (let rate in rateMap) {
        rate = parseInt(rate);
        if (rate >= minRate && rate <= maxRate) {
          range.push(rateMap[rate]);
        }
      }
      return range.join(', ');
    }
  }
}
</script>

<style scoped>
.reference-example-container {
  height: 100%;
}

.el-header {
  background-color: #143FAE;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 24px;
}

.main {
  position: relative;
  height: calc(100vh - 120px);
}

.content {
  padding: 20px;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100% - 100px);
}

.demo-image__preview {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
  max-width: 50%;
}

.demo-image {
  max-width: 100%;
  height: auto;
}

.text-container {
  flex: 1;
  max-width: 50%;
  padding-left: 20px;
  text-align: left;
}

.buttons-pagination-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
}

.pagination {
  order: 2;
}

.button-container {
  order: 1;
  display: flex;
  justify-content: center;
  width: 100%;
}

.el-tag + .el-tag {
  margin-left: 10px;
}
</style>
