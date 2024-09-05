<template>
  <el-container>
    <el-header>
      <div>Macro Photography IQA</div>
      <div>{{ userId }}</div>
    </el-header>
    <el-main class="main">
      <div class="content">
        <div class="demo-image__preview">
          <img :src="currentImageUrl" class="image" ref="imageElement">
        </div>
        <el-tabs class="tabs" type="border-card" :tab-position="tabPosition">
          <el-tab-pane label="Rating">
            <div class="block">
              <div class="rating-status">
                <span>If Rated:</span>
                <i v-if="isRated" class="el-icon-check completed"></i>
                <i v-else class="el-icon-close not-completed"></i>
              </div>
              <el-slider :step="25" v-model="value" vertical height="200px" :marks="marks">
              </el-slider>
              <el-button class="save-button" type="primary" round @click="saveRating(false)">Save</el-button>
            </div>
          </el-tab-pane>
          <el-tab-pane label="Annotation">
            <div style="overflow-y: auto; height: 500px;">
              <div>
                <el-button type="primary" round @click="addRow">Add</el-button>
                <div v-for="(row, index) in rows" :key="index">
                  This image is
                  <el-select v-model="row.magnitude" placeholder="Select" size="mini">
                    <el-option v-for="item in options1" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-select>
                  <el-select v-model="row.factor" placeholder="Select" size="mini">
                    <el-option v-for="item in options2" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-select>
                  in
                  <el-select v-model="row.position" placeholder="Select" size="mini">
                    <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-select>
                  position.
                  <el-button type="danger" size="mini" @click="removeRow(index)">Delete</el-button>
                </div>
              </div>
              <div style="margin: 20px 0;"></div>
              <div>
                <el-input type="textarea" autosize placeholder="Anything else..." v-model="textarea1">
                </el-input>
              </div>
              <div style="margin: 20px 0;"></div>
              <el-button class="save-button" type="primary" round @click="saveAnnotation">Save</el-button>
              <div style="margin: 20px 0;"></div>
              <el-collapse v-model="activeName" accordion>
                <el-collapse-item title="Overexposure (too bright)" name="1">
                  <div>Image becomes excessively bright or loses detail due to prolonged exposure time or excessive
                    light.
                  </div>
                </el-collapse-item>
                <el-collapse-item title="Underexposure (insufficient light)" name="2">
                  <div>Image becomes excessively dark or lacks clarity due to insufficient exposure.</div>
                </el-collapse-item>
                <el-collapse-item title="Out of focus" name="3">
                  <div>Image lacks clarity due to the lens not being properly focused.</div>
                </el-collapse-item>
                <el-collapse-item title="Blur" name="4">
                  <div>Image lacks detail due to camera or subject movement during the capture.</div>
                </el-collapse-item>
                <el-collapse-item title="Low resolution" name="5">
                  <div>Image has fewer pixels, resulting in a lack of clarity or distortion in the image details.</div>
                </el-collapse-item>
                <el-collapse-item title="Noisy and grainy" name="6">
                  <div>The presence of random colors or grain-like interference in an image, resulting in distortion or
                    lack of clarity in the image details.
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-main>
    <el-footer class="footer">
      <div class="button-group-left">
        <el-button type="primary" round @click="goToMenuPage">Menu</el-button>
        <el-button type="primary" round @click="goToResultPage">Result</el-button>
      </div>
      <el-pagination
          class="pagination"
          :background="true"
          layout="prev, pager, next"
          :total="total"
          :page-size="pageSize"
          @current-change="handlePageChange"
          :current-page="currentPage"
      ></el-pagination>
      <div class="button-group-right">
        <el-button type="primary" round @click="goToReferenceIntroPage">Introduction</el-button>
        <el-button type="primary" round @click="goToReferenceExamplePage">Examples</el-button>
      </div>
    </el-footer>
  </el-container>
</template>

<script>
import axios from 'axios';
import {Message} from 'element-ui';

export default {
  created() {
    this.userId = this.$route.params.id;
    this.batch = this.$route.params.batch;
    this.fetchImageData();
  },
  data() {
    return {
      activeName: '0',
      dynamicTags: [],
      rows: [],
      options1: [
        {value: 'slightly', label: 'slightly'},
        {value: 'medially', label: 'medially'},
        {value: 'strongly', label: 'strongly'},
      ],
      options2: [
        {value: 'overexposure', label: 'overexposure'},
        {value: 'underexposure', label: 'underexposure'},
        {value: 'out of focus', label: 'out of focus'},
        {value: 'blur', label: 'blur'},
        {value: 'low resolution', label: 'low resolution'},
        {value: 'noisy and grainy', label: 'noisy and grainy'},
      ],
      options3: [
        {value: 'center', label: 'center'},
        {value: 'top left', label: 'top left'},
        {value: 'top right', label: 'top right'},
        {value: 'bottom left', label: 'bottom left'},
        {value: 'bottom right', label: 'bottom right'},
        {value: 'whole image', label: 'whole image'},
      ],
      inputVisible: false,
      textarea1: '',
      inputValue: '',
      userId: null,
      batch: null,
      tabPosition: 'top',
      value: 50,
      marks: {
        0: 'Bad',
        25: 'Poor',
        50: 'Fair',
        75: 'Good',
        100: 'Excellent'
      },
      result: '',
      fit: 'contain',
      currentImageUrl: '',
      srcList: [],
      images: [],
      total: 0,
      currentPage: 1,
      pageSize: 1,
    };
  },
  watch: {
    currentPage() {
      this.updateCurrentImage();
    }
  },
  computed: {
    paginatedImages() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.images.slice(start, end);
    },
    isRated() {
      const currentImage = this.paginatedImages[0];
      return currentImage && currentImage.rate !== undefined && currentImage.rate !== "NULL";
    }
  },
  methods: {
    fetchImageData() {
      axios.get(`http://127.0.0.1:5001/get_image/${this.userId}`, {
        params: {
          batch: this.batch
        }
      })
          .then(response => {
            const data = response.data;
            this.images = data;
            this.total = data.length;
            if (data.length > 0) {
              const firstUnratedIndex = data.findIndex(image => image.rate === undefined || image.rate === "NULL");
              if (firstUnratedIndex !== -1) {
                this.handlePageChange(firstUnratedIndex + 1);
              } else {
                this.handlePageChange(1);
              }
            }
          })
          .catch(error => {
            console.error('Error fetching image data:', error);
          });
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.updateCurrentImage();
    },
    updateCurrentImage() {
      const currentImage = this.paginatedImages[0];
      this.currentImageUrl = currentImage ? currentImage.url : '';
      this.value = currentImage && currentImage.rate !== undefined && currentImage.rate !== "NULL" ? currentImage.rate : null;
      this.rows = currentImage && currentImage.tagList ? currentImage.tagList : [];
      this.textarea1 = currentImage && currentImage.description !== "NULL" ? currentImage.description : '';
      this.$nextTick(() => {
        this.setImageDimensions();
      });
    },
    setImageDimensions() {
      const img = this.$refs.imageElement;
      if (img && img.complete) {
        const originalWidth = img.naturalWidth;
        const originalHeight = img.naturalHeight;
        img.style.width = `${originalWidth}px`;
        img.style.height = `${originalHeight}px`;
      }
    },
    saveRating(jump = false) {
      const imageId = this.paginatedImages[0].image_id;

      if (this.value === null) {
        this.value = 50;
      }
      axios.post(`http://127.0.0.1:5001/submit_rate/${this.userId}`, {
        batch: this.batch,
        image_id: imageId,
        rate: this.value
      })
          .then(response => {
            if (response.status === 200) {
              Message.success('Rating saved successfully');
              this.paginatedImages[0].rate = this.value;
              if (jump) {
                this.fetchImageData();
              } else {
                this.updateCurrentImage();
              }
            } else {
              Message.error('Failed to save rating');
            }
          })
          .catch(error => {
            console.error('Error saving rating:', error);
            Message.error('Error saving rating');
          });
    },
    saveAnnotation() {
      const imageId = this.paginatedImages[0].image_id;
      axios.post(`http://127.0.0.1:5001/update_data/${this.userId}`, {
        image_id: imageId,
        tagList: this.rows,
        description: this.textarea1
      })
          .then(response => {
            if (response.status === 200) {
              Message.success('Annotation saved successfully');
              this.paginatedImages[0].tagList = this.rows;
              this.paginatedImages[0].description = this.textarea1;
              this.updateCurrentImage();
            } else {
              Message.error('Failed to save annotation');
            }
          })
          .catch(error => {
            console.error('Error saving annotation:', error);
            Message.error('Error saving annotation');
          });
    },
    goToReferenceIntroPage() {
      this.$router.push({name: 'ReferenceIntro', params: {id: this.userId, batch: this.batch}});
    },
    goToReferenceExamplePage() {
      this.$router.push({name: 'ReferenceExample', params: {id: this.userId, batch: this.batch}});
    },
    goToMenuPage() {
      this.$router.push({name: 'MenuPage', params: {id: this.userId}});
    },
    goToResultPage() {
      this.$router.push({name: 'ResultPage', params: {id: this.userId}});
    },
    addRow() {
      this.rows.push({magnitude: '', factor: '', position: []});
    },
    removeRow(index) {
      this.rows.splice(index, 1);
    }
  }
}
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
  overflow: hidden;
}

.content {
  padding: 0;
  margin: 0;
  display: flex;
  height: calc(100% - 80px);
  align-items: flex-start;
}

.demo-image__preview {
  flex: 1;
  margin-right: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image {
  object-fit: contain;
}

.tabs {
  flex: 0.3;
  margin-right: 20px;
}

.rating-status {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.status-indicator {
  font-size: 50px;
  margin-left: 10px;
}

.completed {
  color: green;
}

.not-completed {
  color: red;
}

.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background-color: #F2F6FC;
}

.button-group-left, .button-group-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pagination {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.block {
  display: flex;
  flex-direction: column;
}

.save-button {
  align-self: flex-end;
}

.el-tag + .el-tag {
  margin-left: 10px;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>
