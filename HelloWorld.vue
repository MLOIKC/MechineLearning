<template>
  <el-card class="box-card" shadow="always">
    <div class="common-layout">
      <el-container>
        <el-header>
          <h1>
            <h3>机器学习模型训练器</h3>
          </h1>
        </el-header>
        <el-container>
          <el-aside width="700px">
            <!-- 模型 -->
            <div>
              <h3>请选择需要验证的模型：</h3>
              <div v-if="modelList.length === 0">没有模型</div>
              <!-- <el-radio-group v-model="modelName">
        <el-radio v-for="(name, idx) in modelList" :key="name" :label="name">{{ name }}</el-radio>
      </el-radio-group> -->
              <el-select v-model="modelName" class="m-2" placeholder="Select" size="large">
                <el-option v-for="(name, idx) in modelList" :key="name" :label="name" :value="name" />
              </el-select>
            </div>
            <div>
              <!-- 数据集 -->
              <!-- <div>
      <h2>数据集</h2>
      <div v-if="datasetList.length === 0">没有数据集</div>
      <el-radio-group v-model="datasetName">
        <el-radio v-for="(name, idx) in datasetList" :key="name" :label="name">{{ name }}</el-radio>
      </el-radio-group>
    </div> -->

              <!-- <div class="example-block">
    <span class="example-demonstration"><h2>数据集</h2></span>
    <div v-if="datasetList.length === 0">没有数据集</div>
    <el-cascader v-model="datasetName" :options="options" @change="handleChange" /> -->
              <h3>请选择合适的数据集：</h3>
              <div v-if="datasetList.length === 0">没有数据集</div>
              <el-select v-model="datasetName" class="m-2" placeholder="Select" size="large">
                <el-option v-for="(name, idx) in datasetList" :key="name" :label="name" :value="name" />
              </el-select>
            </div>
            <!-- 数据集切分器 -->
            <div>
              <h3>请选择合适的数据集切分器：</h3>
              <div v-if="splitterList.length === 0">没有数据集切分器</div>
              <!-- <el-radio-group v-model="splitterName">
        <el-radio v-for="(name, idx) in splitterList" :key="name" :label="name">{{ name }}</el-radio>
      </el-radio-group> -->
              <el-select v-model="splitterName" class="m-2" placeholder="Select" size="large">
                <el-option v-for="(name, idx) in splitterList" :key="name" :label="name" :value="name" />
              </el-select>
            </div>

            <!-- <el-divider /> -->


            <!-- 结果判别器 -->
            <div>
              <h3>请选择合适的结果判别器：</h3>
              <div v-if="judgerList.length === 0">没有结果判别器</div>
              <!-- <el-radio-group v-model="judgerName">
        <el-radio v-for="(name, idx) in judgerList" :key="name" :label="name">{{ name }}</el-radio>
      </el-radio-group> -->
              <el-select v-model="judgerName" class="m-2" placeholder="Select" size="large">
                <el-option v-for="(name, idx) in judgerList" :key="name" :label="name" :value="name" />
              </el-select>
            </div>
            <h2></h2>
            <el-button @click="clickButton" size="large" color="#268bff" plain>
              <h2>点击此按钮运行</h2>
            </el-button>

            <div>
              <h3></h3>
            </div>
          </el-aside>

          <el-main>

            <div>
              <h2>运行结果</h2>
              <div class="running-res">
                <div v-for="(content, idx) in runningOutput" :key="idx">{{ content }}</div>
              </div>
            </div>

          </el-main>

        </el-container>
      </el-container>
    </div>
  </el-card>

  <!-- <el-divider /> -->


</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { DEFAULT_DYNAMIC_LIST_ITEM_SIZE } from 'element-plus/es/components/virtual-list/src/defaults';
import { reactive, ref } from 'vue'

let ws: WebSocket = new WebSocket('ws://localhost:8765')
ws.onopen = () => {
  ws.send(JSON.stringify({
    'type': 'overview',
    'params': {}
  }))
}
ws.onmessage = (evt) => {
  var received_msg = JSON.parse(evt.data);
  // console.log(received_msg);

  if (received_msg.status === 200) {
    const received_msg_data = received_msg.data
    if (received_msg.type === 'overview') {
      datasetList.value = received_msg_data.datasets
      splitterList.value = received_msg_data.splitters
      modelList.value = received_msg_data.models
      judgerList.value = received_msg_data.judgers
    }

    else if (received_msg.type === 'print') {
      runningOutput.value.push(received_msg_data.content as never)
    }
  } else {
    console.error(received_msg.data);
  }
}

const datasetName = ref(null)
const datasetList = ref([])

const splitterName = ref(null)
const splitterList = ref([])

const modelName = ref(null)
const modelList = ref([])

const judgerName = ref(null)
const judgerList = ref([])

const clickButton = () => {
  if (!datasetName.value || !splitterName.value || !modelName.value || !judgerName.value) {
    ElMessage.error('您的选项不完整')
    return
  }
  runningOutput.value = []
  ws.send(JSON.stringify({
    'type': 'run',
    'params': {
      'datasetName': datasetName.value,
      'splitterName': splitterName.value,
      'modelName': modelName.value,
      'judgerName': judgerName.value
    }
  }))
}

const runningOutput = ref([])



// const props = {
//   expandTrigger: 'hover',
// }

// const handleChange = (datasetName:any) => {
//   console.log(datasetName)
// }

// const options = [
//   {
//     value: 'guide',
//     label: '线性回归模型',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '支持向量机',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: 'k-近邻算法',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '逻辑回归算法',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '决策树算法',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '分类和聚类',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '概率图模型',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '集成学习与随机森林',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '贝叶斯分类器',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '降维与度量学习',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '梯度增强',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: '强化学习',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
//   {
//     value: 'guide',
//     label: 'XGboost算法',
//     children: [
//       {
//         value: 'disciplines',
//         label: '数据集1',
//       },
//       {
//         value: 'navigation',
//         label: '数据集2',
//       },
//       {
//         value: 'navigation',
//         label: '数据集3',
//       },
//     ],
//   },
// ]



</script>

<style scoped>
.running-res {
  text-align: left;
  width: 100%;
  font-size: large;
}

/* .example-block {
  margin: 5rem;
}
.example-demonstration {
  margin: 1rem;
} */
.text {
  font-size: 14px;
}

.item {
  padding: 18px 0;
}

.box-card {
  width: 1400px;
  background-color: rgb(245, 253, 255);
  margin: 50px;
  border-radius: 60px;
  border-color: #268bff;
}
</style>
