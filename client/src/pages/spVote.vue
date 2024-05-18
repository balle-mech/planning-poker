<template>
  <h2>投票ページ</h2>

  <!--PC用 -->
  <div class="form_container form_container_PC">
    <form @submit.prevent="spChange" class="form">
      <v-container>
        <v-row>
          <v-col cols="3"></v-col>
          <v-col cols="6">
            <v-select v-model="selectedName" :items="nameList" label="名前を選択してください">
            </v-select>
            <input v-if="selectedName === newName" v-model="newUser" required placeholder="ユーザー名を入力してください"
              class="input_name" />
          </v-col>
          <v-col cols="3"></v-col>
        </v-row>
        <v-row>
          <v-col cols="3"></v-col>
          <v-col cols="6">
            <v-select v-model="newSp" :items="fibonacciList" label="SPを選択してください">
            </v-select>
          </v-col>
          <v-col cols="3"></v-col>
        </v-row>
      </v-container>
      <button class="button enter_button">投票する</button>
    </form>
  </div>
  <!-- スマホ用 -->
  <div class="form_container form_container_phone">
    <form @submit.prevent="spChange" class="form">
      <v-container>
        <v-row>
          <v-col cols="1"></v-col>
          <v-col cols="10">
            <v-select v-model="selectedName" :items="nameList" label="名前を選択してください">
            </v-select>
            <input v-if="selectedName === newName" v-model="newUser" required placeholder="ユーザー名を入力してください"
              class="input_name" />
          </v-col>
          <v-col cols="1"></v-col>
        </v-row>
        <v-row>
          <v-col cols="1"></v-col>
          <v-col cols="10">
            <v-select v-model="newSp" :items="fibonacciList" label="SPを選択してください">
            </v-select>
          </v-col>
          <v-col cols="1"></v-col>
        </v-row>
      </v-container>
      <button class="button enter_button">投票する</button>
    </form>
  </div>

  <!-- 投票結果の表示機能 -->
  <div>
    <button @click="isShowingSp ? hiddenSp() : showSp()" class="button show_button">
      {{ isShowingSp ? "閉じる" : "投票結果" }}
    </button>
    <div v-if="isShowingSp">
      <!-- ロード中表示 -->
      <div v-if="isLoading">Now Loading...</div>
      <!-- ロード終了後 -->
      <div v-else>
        <h2 v-if="!awesome2" class="text_load">ネットワークの接続を確認してください</h2>
        <h2 v-if="awesome2 && !awesome" class="text_load">投票データがありません</h2>
        <table class="vote_table">
          <thead>
            <tr>
              <th v-if="awesome2 && awesome">NAME</th>
              <th v-if="awesome2 && awesome">SP</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="spData in spList" :key="spData.id">
              <td>{{ spData.user_name }}</td>
              <td>{{ spData.user_sp }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <!-- PBL一覧へ戻るボタンの表示 -->
  <div class="back">
    <router-link :to="{ path: './' }" class="back_text">戻る</router-link>
  </div>
</template>

<script setup>
import { ref, inject, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

/* axiosと動的リンク関係 */
const axios = inject("axios");
const route = useRoute();
const id = route.params.backlogId;

/* データが有るかの判定用変数(データがなければfalse) */
const awesome = ref(false);
/* ネットワークリンクの確認用変数(リンク接続できなければfalse) */
const awesome2 = ref(false);
/* 読み込み中か否かの判定用変数(読み込み中ならtrue)*/
const isLoading = ref(true);

/* 既存の名前の場合 */
const selectedName = ref("");

/* 新規ユーザー */
const newUser = ref("");

/* 提案SP */
const newSp = ref("");

/* 未定義ユーザー */
const newName = "新規ユーザー";

/* 名前リスト */
const nameList = ref([]);

/* 名前リスト(重複を許さないset型) */
const nameSet = new Set();

/* データ一式 */
const spList = ref([]);

/* id一式(これがないと上書きができないはず？) */
const idList = ref(new Object());

/* フィボナッチ数列 */
const fibonacciList = [0.5, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89];

/* 条件分け用の変数 */
let flag = 0;

// モード切替の状態管理
const isShowingSp = ref(false);

const hiddenSp = () => {
  isShowingSp.value = false;
};

/* 提示SPの一括取得 */
function getData() {
  axios
    .get("http://localhost:3000/api/pbls/view_offered_sp/" + id)
    .then((response) => {
      spList.value = response.data;

      /* 正常取得判定 */
      if (response.status == 200) {
        awesome2.value = true
      }

      if (spList.value.length == 0) {
        awesome.value = false;
      } else {
        awesome.value = true;
      }
      for (var i = 0; i < spList.value.length; i++) {
        if (!nameSet.has(String(spList.value[i].user_name))) {
          nameSet.add(spList.value[i].user_name);
          nameList.value.push(spList.value[i].user_name);
          idList.value[spList.value[i].user_name] = spList.value[i].id;
        }
      }
      /* 新規ユーザー */
      nameList.value.push(newName);

      /* 視認性のためのソート */
      spList.value.sort(function (item1, item2) {
        return item1.user_sp - item2.user_sp;
      });
    })

    .finally(() => {
      isLoading.value = false;
      console.log(nameList)
    });
}

/* 開示 */
const showSp = () => {
  /* フォームに文字がない場合の処理 */
  if (selectedName.value == "" && newSp.value == "") {

    /* 情報の再取得 */
    nameList.value = [];
    idList.value = {};
    nameSet.clear();

    getData();

    isShowingSp.value = true;
  } else {
    /* フォームに文字がある場合の処理 */
    var result = window.confirm("投票を中止して投票状況を閲覧しますか？");

    /* 投票中止 */
    if (result) {
      selectedName.value = "";
      newUser.value = "";
      newSp.value = "";

      setTimeout(showSp, 0.1);
    } else {
      /* 続行 */
    }
  }
};

onMounted(() => {
  /* 変数の監視 */
  watch(selectedName, () => {
    newUser.value = "";
    hiddenSp();
  });

  watch(newSp, () => {
    hiddenSp();
  });

  getData();
});

/* 投票 */
function spChange() {
  if (
    selectedName.value == "" ||
    newSp == "" ||
    (selectedName.value == newName && newUser == "")
  ) {
    window.alert(
      "不正な入力です、以下の条件を満たすこと確認してください\n\n" +
      "・ユーザーが指定されていること\n・ユーザー名は1文字以上10文字以下であること\n・SPが選択されていること"
    );
  } else if (
    /* 新規ユーザー時処理(すでにある名前をいれた場合は既存ユーザとして扱う)*/
    selectedName.value == newName &&
    !nameSet.has(String(newUser.value))
  ) {
    var postData = {
      user_name: String(newUser.value),
      user_sp: String(newSp.value),
      backlog_id: String(id),
    };

    /* 処理可能な場合 (1文字以上、10文字以下かつSPが選択されている)*/
    if (
      1 <= postData.user_name.length &&
      postData.user_name.length <= 10 &&
      postData.user_sp != ""
    ) {
      flag = 1;

      axios.post(
        "http://localhost:3000/api/pbls/register_offered_sp",
        JSON.stringify(postData)
      );
    } else {
      /* 条件を満たさない場合 */
      window.alert(
        "不正な入力です、以下の条件を満たすこと確認してください\n\n" +
        "・ユーザーが指定されていること\n・ユーザー名は1文字以上10文字以下であること\n・SPが選択されていること"
      );
    }
  } else {
    /* 既存ユーザ */
    /* 新規ユーザーを選んだが、既存ユーザーだった場合のデータ */
    if (selectedName.value == newName) {
      /* 処理可能な場合 (1文字以上、10文字以下かつSPが選択されている)*/
      if (
        1 <= newUser.value.length &&
        newUser.value.length <= 10 &&
        newSp.value != ""
      ) {
        var postData = {
          id: idList.value[newUser.value],
          user_sp: newSp.value,
        };

        flag = 1;

        axios.post(
          "http://localhost:3000/api/pbls/update_offered_sp",
          JSON.stringify(postData)
        );
      } else {
        /* 不適切な入力 */
        window.alert(
          "不正な入力です、以下の条件を満たすこと確認してください\n\n" +
          "・ユーザーが指定されていること\n・ユーザー名は1文字以上10文字以下であること\n・SPが選択されていること"
        );
      }
    } else {
      /* 既存ユーザを選んだ場合 */
      if (newSp.value != "") {
        var postData = {
          id: idList.value[selectedName.value],
          user_sp: newSp.value,
        };

        flag = 1;

        axios.post(
          "http://localhost:3000/api/pbls/update_offered_sp",
          JSON.stringify(postData)
        );
      } else {
        /* 不適切な入力 */
        window.alert(
          "不正な入力です、以下の条件を満たすこと確認してください\n\n" +
          "・ユーザーが指定されていること\n・ユーザー名は1文字以上10文字以下であること\n・SPが選択されていること"
        );
      }
    }
  }

  /* 初期化 */
  selectedName.value = "";
  newUser.value = "";
  newSp.value = "";

  /* 情報の更新があった場合の処理 */
  if (flag == 1) {
    /* 情報の再取得 */
    nameList.value = [];
    idList.value = {};
    nameSet.clear();

    getData();
    flag = 0;
  }
}
</script>

<style scoped>
.form_container {
  width: 80vw;
  max-width: 900px;
}

.form {
  width: 100%;
}

.vote_container {
  width: 100%;
}

.input_name {
  background: #eee;
  height: 50px;
  width: 200px;
  border-radius: 8px;
  padding-left: 0.5em;
}

::placeholder {
  color: gray;
}

.show_button {
  margin-top: 20px;
}

.button {
  width: 120px;
  color: #fff;
  border: 3px solid #fff;
  background: rgba(0, 64, 152, 1);
  border-radius: 8px;
  transition: 0.3s;
  font-size: 14px;
  font-weight: bold;
}

.button:hover {
  color: rgba(0, 64, 152, 1);
  background: #fff;
  border: 3px solid rgba(0, 64, 152, 1);
}

.text_load {
  margin-top: 50px;
}

.vote_table {
  margin: 50px auto;
  border-collapse: collapse;
  width: 300px;
  text-align: center;
  box-sizing: border-box;
}


th,
td {
  border: 1px solid black;
  padding: 10px;
}

thead {
  background: lightgray;
}

.back {
  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
}

@media (min-width: 751px) {
  .form_container_phone {
    display: none !important;
  }
}

@media (max-width: 750px) {
  .form_container_PC {
    display: none !important;
  }
}
</style>
