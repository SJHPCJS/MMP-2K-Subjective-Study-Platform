<template>
    <el-container>
        <el-header>
            <div>Macro Photography IQA</div>
            <div>{{ userId }}</div>
        </el-header>
        <el-main class="main">
            <div class="content">
                <div class="demo-image__preview">
                    <el-image :src="url" :preview-src-list="srcList" :fit="fit">
                    </el-image>
                </div>
                <el-tabs class="tabs" type="border-card" :tab-position="tabPosition">
                    <el-tab-pane label="Rating">
                        <div class="block">
                            <el-slider step="25" v-model="value" vertical height="200px" :marks="marks" @change = handleChange>
                            </el-slider>
                            <el-button class="save-button" type="primary" round @click="open" plain>Save</el-button>
                        </div>
                    </el-tab-pane>
                    <el-tab-pane label="Annotation">
            <div style="overflow-y: auto; height: 680px;">
              <div>
                <el-button type="primary" round @click="addRow">Add</el-button>
                <div v-for="(row, index) in rows" :key="index">
                  This image is
                  <el-select v-model="row.select1" placeholder="Select" size="mini">
                    <el-option v-for="item in options1" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-select>
                  <el-select v-model="row.select2" placeholder="Select" size="mini">
                    <el-option v-for="item in options2" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-select>
                  in
                  <el-select v-model="row.select3" multiple placeholder="Select" size="mini">
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
              <el-button class="save-button" type="primary" round @click="goToTrainPage">Save</el-button>
              <div style="margin: 20px 0;"></div>
              <!-- <el-tag :key="tag" v-for="tag in dynamicTags" closable :disable-transitions="false"
                @close="handleClose(tag)">
                {{ tag }}
              </el-tag>
              <el-select v-if="inputVisible" v-model="inputValue" ref="saveTagInput" size="small"
                @change="handleInputConfirm">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
              <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button> -->
              <el-collapse v-model="activeName" accordion>
                <el-collapse-item title="Overexposure (too bright)" name="1">
                  <div>Image becomes excessively bright or loses detail due to prolonged exposure time or excessive light.</div>
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
                  <div>The presence of random colors or grain-like interference in an image, resulting in distortion or lack of clarity in the image details.</div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </el-tab-pane>
                </el-tabs>
            </div>

            <div class="buttons-pagination-container">
                <el-pagination class="pagination" background="true" layout="prev, pager, next"
                    :total="1000"></el-pagination>
                <div>
                    <el-button type="primary" round @click="goToMenuPage">Menu</el-button>
                    <el-button type="primary" round @click="goToResultPage">Result</el-button>
                </div>

                <el-pagination class="pagination" background layout="prev, pager, next" :total="1000"></el-pagination>
                <div>
                    <el-button type="primary" round @click="goToReferenceIntroPage">Introduction</el-button>
                    <el-button type="primary" round @click="goToReferenceExamplePage">Examples</el-button>
                    <el-button type="primary" round @click="goToMenuPage">Finish training</el-button>
                </div>
            </div>

        </el-main>
    </el-container>
</template>

<script>
export default {
    created() {
        this.userId = this.$route.params.id;
    },
    data() {
        return {
            activeName: '0',
      dynamicTags: [],
      rows: [],
      options1: [
        { value: 'slightly', label: 'slightly' },
        { value: 'medially', label: 'medially' },
        { value: 'strongly', label: 'strongly' },
      ],
      options2: [
        { value: 'oversxposure', label: 'oversxposure' },
        { value: 'underexposure', label: 'underexposure' },
        { value: 'out of focus', label: 'out of focus' },
        { value: 'blur', label: 'blur' },
        { value: 'low resolution', label: 'low resolution' },
        { value: 'noisy and grainy', label: 'noisy and grainy' },
      ], options3: [
        { value: 'center', label: 'center'},
        { value: 'top left', label: 'top left' },
        { value: 'top right', label: 'top right' },
        { value: 'bottom left', label: 'bottom left' },
        { value: 'bottom right', label: 'bottom right' },
        { value: 'whole image', label: 'whole image' },
        
      ],
      inputVisible: false,
      textarea: '',
      inputValue: '',
      userId: null,
      tabPosition: 'top',
      value: 50,
      marks: {
        0: 'Bad',
        25: 'Poor',
        50: 'Fair',
        75: 'Good',
        100: 'Excellent'
      },
      mark:'',
      fits: 'contain',
      url: require("../assets/background.jpg"),
      srcList: [require("../assets/background.jpg")]
        };
    },
    methods: {
        goToReferenceIntroPage() {
      this.$router.push({ name: 'ReferenceIntro', params: { id: this.userId } });
    },
    goToReferenceExamplePage() {
      this.$router.push({ name: 'ReferenceExample', params: { id: this.userId } });
    },
    goToMenuPage() {
      this.$router.push({ name: 'MenuPage', params: { id: this.userId } });
    },
    goToResultPage() {
      this.$router.push({ name: 'ResultPage', params: { id: this.userId } });
    },
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
    },
    showInput() {
      this.inputVisible = true;
      // eslint-disable-next-line
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.dynamicTags.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = '';
    },
    addRow() {
      this.rows.push({ select1: '', select2: '', select3: '' });
    },
    removeRow(index) {
      this.rows.splice(index, 1);
    },
    handleChange(val) {
      this.mark = val;
    },
    open() {
    let type = this.mark === 50 ? 'success' : 'warning';
    this.$notify({
        title: 'Test',
        message: 'The mark should be 50',
        type: type
    });
},

  }
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

.main {
    position: relative;
    height: calc(100vh - 120px);
}

.content {
    padding: 20px;
    margin: 0;
    flex-direction: row;
    display: flex;
    height: calc(100% - 100px);

}

.demo-image__preview {
    flex: 1;
    margin-right: 20px;
    overflow: auto;
}

.tabs {
    flex: 0.3;
    margin-right: 20px;
}

.collapse {
    margin-top: 40px;
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

.button-group-left {
    order: 1;
}

.button-group-right {
    order: 3;
}

.pagination {
    position: absolute;
    bottom: 50px;
    left: 50%;
    transform: translateX(-50%);
}

.block {
    display: flex;
    flex-direction: column;
}

.save-button {
    align-self: flex-end;
}
</style>