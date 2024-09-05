<template>
  <el-container>
    <el-header>
      <div>Macro Photography IQA</div>
      <div>{{ userId }}</div>
    </el-header>
    <el-main>
      <h1>Thank you for your efforts!</h1>
      <div class="done">
        <el-progress type="circle" :percentage="part1" :status="part1Status" :width="200">
          <span slot="content">segment1</span>
        </el-progress>
        <el-progress type="circle" :percentage="part2" :status="part2Status" :width="200">
          <span slot="content">segment2</span>
        </el-progress>
        <el-progress type="circle" :percentage="part3" :status="part3Status" :width="200">
          <span slot="content">segment3</span>
        </el-progress>
        <el-progress type="circle" :percentage="part4" :status="part4Status" :width="200">
          <span slot="content">segment4</span>
        </el-progress>
      </div>
      <div style="display: flex; justify-content: space-around; background-color: #FFFFFF;">
        <div>batch1</div>
        <div>batch2</div>
        <div>batch3</div>
        <div>batch4</div>
      </div>
      <div class="button">
        <el-button type="primary" round @click="goToMenuPage">Go to menu</el-button>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ResultPage',
  created() {
    this.userId = this.$route.params.id;
    this.fetchResultData();
    this.startPolling();
  },
  beforeRouteUpdate(to, from, next) {
    this.userId = to.params.id;
    this.fetchResultData();
    next();
  },
  beforeDestroy() {
    clearInterval(this.pollingInterval);
  },
  data() {
    return {
      userId: null,
      part1: 0,
      part2: 0,
      part3: 0,
      part4: 0,
      pollingInterval: null,
    };
  },
  computed: {
    part1Status() {
      return this.part1 === 100 ? 'success' : '';
    },
    part2Status() {
      return this.part2 === 100 ? 'success' : '';
    },
    part3Status() {
      return this.part3 === 100 ? 'success' : '';
    },
    part4Status() {
      return this.part4 === 100 ? 'success' : '';
    },
  },
  methods: {
    fetchResultData() {
      console.log(`Fetching result data for user: ${this.userId}`);
      axios.get(`http://localhost:5001/result/${this.userId}`)
          .then(response => {
            const result = response.data.result;
            console.log("Received result data:", result);
            this.part1 = result["1"] || 0;
            this.part2 = result["2"] || 0;
            this.part3 = result["3"] || 0;
            this.part4 = result["4"] || 0;
          })
          .catch(error => {
            console.error('Error fetching result data:', error);
          });
    },
    startPolling() {
      this.pollingInterval = setInterval(() => {
        this.fetchResultData();
      }, 5000); // 每5秒轮询一次
    },
    goToMenuPage() {
      this.$router.push({name: 'MenuPage', params: {id: this.userId}});
    },
  }
  ,
}
</script>

<style>
.el-header {
  background-color: #143FAE;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 24px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  height: calc(100vh - 60px);
  line-height: auto;
}

.done {
  background-color: #FFFFFF;
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.button {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
