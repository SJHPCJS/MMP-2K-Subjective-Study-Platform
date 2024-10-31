<template>
  <el-container>
    <el-header>
      <div>Macro Photography IQA</div>
      <div>{{ userId }}</div>
    </el-header>
    <el-main class="main">
      <div class="content">
        <div class="demo-image__preview">
          <img :src="getImageUrl(currentImageId)" class="image" ref="imageElement">
        </div>
        <el-tabs class="tabs" type="border-card" :tab-position="tabPosition" v-model="activeTab">
          <!-- Rating Tab -->
          <el-tab-pane label="Rating" name="Rating">
            <div class="block">
              <el-slider :step="25" v-model="value" vertical height="200px" :marks="marks"></el-slider>
              <el-button class="save-button" type="primary" round @click="checkRating">Save</el-button>
            </div>
          </el-tab-pane>

          <!-- Annotation Tab -->
          <el-tab-pane label="Annotation" name="Annotation">
            <div class="annotation-content">
              <el-button type="primary" round @click="addRow">Add</el-button>
              <div v-for="(row, index) in rows" :key="index">
                This image is
                <el-select v-model="row.select1" placeholder="Select" size="mini">
                  <el-option v-for="item in options1" :key="item.value" :label="item.label" :value="item.value"></el-option>
                </el-select>
                <el-select v-model="row.select2" placeholder="Select" size="mini">
                  <el-option v-for="item in options2" :key="item.value" :label="item.label" :value="item.value"></el-option>
                </el-select>
                in
                <el-select v-model="row.select3" multiple placeholder="Select" size="mini">
                  <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value"></el-option>
                </el-select>
                position.
                <el-button type="danger" size="mini" @click="removeRow(index)">Delete</el-button>
              </div>
              <el-input type="textarea" autosize placeholder="Anything else..." v-model="textarea1" class="textarea"></el-input>
              <el-button class="save-button" type="primary" round @click="saveAnnotation">Save</el-button>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <div class="footer">
        <div class="pagination-container">
          <el-pagination
            class="pagination"
            :background="true"
            layout="prev, pager, next"
            :page-size="1"
            :current-page.sync="currentPage"
            :total="totalImages"
            @current-change="handlePageChange"
          ></el-pagination>
        </div>
        <div class="button-group-right">
          <el-button type="danger" round @click="endTraining">Finish Training</el-button>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import imageInfo from "@/components/train/output_image_info.json";

export default {
  created() {
    console.log("Loading images from JSON file...");
    this.userId = this.$route.params.id;
    this.loadImages();
  },
  data() {
    return {
      userId: null,
      activeTab: 'Rating',
      rows: [],
      options1: [
        { value: 'slightly', label: 'slightly' },
        { value: 'medially', label: 'medially' },
        { value: 'strongly', label: 'strongly' },
      ],
      options2: [
        { value: 'overexposure', label: 'overexposure' },
        { value: 'underexposure', label: 'underexposure' },
        { value: 'out of focus', label: 'out of focus' },
        { value: 'blur', label: 'blur' },
        { value: 'low resolution', label: 'low resolution' },
        { value: 'noisy and grainy', label: 'noisy and grainy' },
      ],
      options3: [
        { value: 'center', label: 'center' },
        { value: 'top left', label: 'top left' },
        { value: 'top right', label: 'top right' },
        { value: 'bottom left', label: 'bottom left' },
        { value: 'bottom right', label: 'bottom right' },
        { value: 'whole image', label: 'whole image' },
      ],
      textarea1: '',
      tabPosition: 'top',
      value: 50,
      marks: {
        0: 'Bad',
        25: 'Poor',
        50: 'Fair',
        75: 'Good',
        100: 'Excellent',
      },
      totalImages: 12,
      currentPage: 1,
      currentImageId: null,
      images: [],
      fit: 'contain',
    };
  },
  methods: {
    loadImages() {
      const imageIds = Object.keys(imageInfo);
      console.log("Image IDs from JSON:", imageIds);
      this.images = imageIds.slice(0, this.totalImages);
      console.log("Loaded images array:", this.images);
      this.updateCurrentImage();
    },
    getImageUrl(imageId) {
      try {
        return require(`@/components/train/${imageId}.jpg`);
      } catch (error) {
        console.error(`Error loading image with ID: ${imageId}`, error);
        return require('@/assets/error.png');
      }
    },
    updateCurrentImage() {
      this.currentImageId = this.images[this.currentPage - 1];
      console.log("Current image ID:", this.currentImageId);

      // 每次切换图片时将分数滑块重置为50
      this.value = 50;
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.updateCurrentImage();
    },
    checkRating() {
      const { lower_bound, upper_bound } = imageInfo[this.currentImageId].score_range;
      if (this.value < lower_bound || this.value > upper_bound) {
        this.$notify({
          title: 'Warning',
          message: `The rating should be between ${lower_bound} and ${upper_bound}`,
          type: 'error',
        });
      } else {
        this.$notify({
          title: 'Success',
          message: 'The rating is within the correct range!',
          type: 'success',
        });
      }
    },
    saveAnnotation() {
      this.$notify({
        title: 'Success',
        message: 'Annotation saved successfully',
        type: 'success',
      });
    },
    endTraining() {
      this.$notify({
        title: 'Training Ended',
        message: 'You have successfully completed the training!',
        type: 'success',
      });
      this.$router.push({ name: 'MenuPage' });
    },
    addRow() {
      this.rows.push({ select1: '', select2: '', select3: '' });
    },
    removeRow(index) {
      this.rows.splice(index, 1);
    },
  },
};
</script>

<style scoped>
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
  height: calc(100% - 100px);
}

.demo-image__preview {
  flex: 1;
  margin-right: 20px;
  overflow: auto;
}

.image {
  max-width: 100%;
  height: auto;
  object-fit: contain;
}

.tabs {
  flex: 0.3;
  margin-right: 20px;
}

.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
}

.pagination-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
}

.button-group-right {
  margin-left: auto;
}

.block {
  display: flex;
  flex-direction: column;
}

.save-button {
  align-self: flex-end;
}
</style>
