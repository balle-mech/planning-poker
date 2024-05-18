<template>
  <!-- ロード中表示 -->
  <div v-if="isLoading">Now Loading...</div>

  <!-- ロード終了後 -->
  <div v-else>

    <h2 class="all_projects" v-if="!awesome2">ネットワークの接続を確認してください</h2>

    <section>

      <h2 class="all_projects" v-if="!awesome && awesome2">プロジェクトが存在しません</h2>
      <h2 class="all_projects" v-if="awesome && awesome2">プロジェクト一覧</h2>
      <table class="table_projects">
        <thead class="thead_projects">
          <tr>
            <th v-if="awesome && awesome2">ID</th>
            <th v-if="awesome && awesome2">プロジェクト</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(project, index) in projects" :key="index">
            <td>{{ project.id }}</td>
            <td> <router-link :to="{ path: '/pbls/' + project.id }" class="ref_projects">{{ project.project_name
                }}</router-link></td>
          </tr>
        </tbody>
      </table>
    </section>

  </div>
</template>


<script setup>
import { ref, inject, onMounted } from "vue";
import { RouterLink } from "vue-router";
const axios = inject("axios");

let projects = ref();

/* データが有るかの判定用変数(データがなければfalse) */
let awesome = ref(false)
/* ネットワークリンクの確認用変数(リンク接続できなければfalse) */
let awesome2 = ref(false)
/* 読み込み中か否かの判定用変数(読み込み中ならtrue)*/
let isLoading = ref(true)

onMounted(() => {
  axios
    .get("http://localhost:3000/api/pbls/view_project_all")
    .then((response) => {

      console.log(response)
      /* 正常取得 */
      if (response.status == 200) {

        awesome2.value = true

        /* データなし */
        if (response.data.length == 0) {

          awesome.value = false

        }

        /* データがあった場合 */
        else {

          awesome.value = true
          projects.value = response.data

        }
      }

      /* ネットワークエラー時 */
      else {
        ;

      }
    })
    /* 画面描画待機用の実装 */
    .finally(() => {

      isLoading.value = false

    });
});

</script>


<style scoped>
.all_projects {
  font-size: 24px;
}

.table_projects {
  margin: 0 auto;
  border-collapse: collapse;
  width: 40vw;
  min-width: 300px;
  text-align: center;
  box-sizing: border-box;
}

th,
td {
  border: 1px solid black;
  padding: 10px;
  height: 60px;
}

.thead_projects {
  background: lightgray;
}

.ref_projects {
  /* background: skyblue; */
  display: inline-block;
  width: 30%;
}



@media(min-width:1000px) {
  .table_projects {
    width: 40vw;

  }

  .ref_projects:hover {
    font-size:1.3em;
    text-decoration: none;
    transition: .3s;
  }
}
</style>