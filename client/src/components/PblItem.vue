<!-- sp未登録の表示とprettierとaddpbl component作成 -->
<template>
  <!-- ロード中表示 -->
  <div v-if="isLoading">Now Loading...</div>

  <!-- 終了後 -->
  <div v-else>
    <h2 v-if="!awesome2">ネットワークの接続を確認してください</h2>
    <h2 v-if="awesome && awesome2">PBL一覧</h2>
    <h2 v-if="!awesome && awesome2">
      このプロジェクトには現段階ではPBLが存在しません
    </h2>
    <!-- 入力フォーム -->
    <div class="button_container">
      <!-- PBL追加画面か否かを変更するボタン -->
      <button @click="isAddingPbl ? cancelAddPbl() : addingPbl()" class="buttons add_button">
        {{ isAddingPbl ? "キャンセル" : "PBL追加" }}
      </button>
      <!-- 三項演算子により編集モードか否かでボタン押下時の呼び出す関数を設定 -->
      <button @click="isEdit ? saveSP() : editing()" class="buttons edit_button">
        {{ isEdit ? "SP保存" : "SP編集" }}
      </button>
    </div>
    <!-- 挿入 -->
    <div v-if="isAddingPbl">
      <div class="form_pbl">
        <form class="add_pbl">
          <p>ID</p>
          <input v-model="PblId" required placeholder="IDを入力してください" class="input_pbl" />
          <p>PBL名</p>
          <input v-model="PblName" required placeholder="PBL名を入力してください" class="input_pbl" maxlength="50"
            @input="charLimit" />
          <p>SPRINT</p>
          <input v-model="PblSprint" required placeholder="該当するSprintを入力してください" class="input_pbl" />
        </form>
        <button class="buttons pbl_button" @click="addPbl">追加する</button>
      </div>
    </div>
    <!-- Sprintを選ぶプルダウン -->
    <div v-if="!(!awesome && awesome2)">
      <select v-model="selectedSprint" class="select_sprint">
        <option disabled value="initial">Sprintを選択してください</option>
        <option v-for="number in sortedSprintList" :key="number">
          {{ number }}
        </option>
      </select>
    </div>

    <!-- PBL一覧画面 -->
    <div>
      <table>
        <thead>
          <tr>
            <!-- この部分も例外処理で制御しています -->
            <th v-if="awesome && awesome2">ID</th>
            <th v-if="awesome && awesome2">PBL</th>
            <th v-if="awesome && awesome2">SP</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(pbl, index) in PblList" :key="index">
            <td v-if="
              selectedSprint == 'initial' ||
              selectedSprint == 'すべてのPBLを表示' ||
              selectedSprint == pbl.pbl_sprint
            " id="pbl_id">
              {{ pbl.pbl_id }}
            </td>
            <td v-if="
              (isEdit || isAddingPbl) &&
              (selectedSprint == 'initial' ||
                selectedSprint == 'すべてのPBLを表示' ||
                selectedSprint == pbl.pbl_sprint)
            " id="pbl_name">
              {{ pbl.pbl_name }}
            </td>
            <td v-else-if="
              !(isEdit || isAddingPbl) &&
              (selectedSprint == 'initial' ||
                selectedSprint == 'すべてのPBLを表示' ||
                selectedSprint == pbl.pbl_sprint)
            " id="pbl_name">
              <router-link :to="{ path: '/pbls/' + id + '/' + pbl.id }" class="ref_pbl">
                {{ pbl.pbl_name }}
              </router-link>
            </td>

            <td v-if="
              !isEdit &&
              (selectedSprint == 'initial' ||
                selectedSprint == 'すべてのPBLを表示' ||
                selectedSprint == pbl.pbl_sprint)
            " id="pbl_sp">
              {{ pbl.pbl_sp }}
            </td>
            <td v-else-if="
              isEdit &&
              (selectedSprint == 'initial' ||
                selectedSprint == 'すべてのPBLを表示' ||
                selectedSprint == pbl.pbl_sprint)
            " id="edit_sp">
              <v-container class="pt-4 pb-0 pl-0 pr-0">
                <v-select v-model="selectedSp[index].pbl_sp" :items="fibonacciList">
                </v-select>
              </v-container>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="back">
    <router-link :to="{ path: '/' }" class="back_text">戻る</router-link>
  </div>
  <div class="back">
    <router-link :to="{ path: '/' }" class="back_text">戻る</router-link>
  </div>
  <!-- ページトップへ戻るボタンの表示 -->
  <!-- <div id="page_top"><a href="#" class="top">ページトップへ</a></div> -->
</template>

<script setup>
import { ref, inject, onMounted } from "vue";
import { useRoute } from "vue-router";

const axios = inject("axios");

/* 動的リンク生成用 */
const route = useRoute();
const id = route.params.pblId;

const PblList = ref([]);
const PblName = ref("");
const PblId = ref("");
const PblSprint = ref(null);
/* この変数を配列にすることでv-selectで別々の値を格納できるように変更 */
const selectedSp = ref([]);

/* データが有るかの判定用変数(データがなければfalse) */
let awesome = ref(false);
/* ネットワークリンクの確認用変数(リンク接続できなければfalse) */
let awesome2 = ref(false);
/* 読み込み中か否かの判定用変数(読み込み中ならtrue)*/
let isLoading = ref(true);
/* idをまとめるためのset */
const idSet = new Set();

// SP変更モード切替の状態管理
const isEdit = ref(false);
// PBL追加モード切替の状態管理
const isAddingPbl = ref(false);

/* フィボナッチ数列 */
const fibonacciList = [0.5, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89];

const flag = ref(false);

/*  SP変更モードへ */
const editing = () => {
  isEdit.value = true;
  isAddingPbl.value = false;
  refresh();
};

/* PBL追加モードへ */
const addingPbl = () => {
  isAddingPbl.value = true;
  isEdit.value = false;
  refresh();
};

/* PBL追加モード取りやめ */
const cancelAddPbl = () => {
  isAddingPbl.value = false;
  PblId.value = "";
  PblName.value = "";
  PblSprint.value = "";
  refresh();
};

function refresh() {
  /* 情報のリフレッシュ */
  selectedSp.value = [];

  for (var i = 0; i < PblList.value.length; i++) {
    // SPが登録されているか否かで条件分岐して登録
    if (PblList.value[i].pbl_sp == null) {
      selectedSp.value.push({
        id: PblList.value[i].id,
        pbl_sp: "SPを選択",
      });
    } else {
      selectedSp.value.push({
        id: PblList.value[i].id,
        pbl_sp: PblList.value[i].pbl_sp,
      });
    }
  }
}

/* 重複を除いたSprintのリスト */
let sprintList = new Set();
sprintList.add("すべてのPBLを表示");

/* 並び変えた重複を除いたSprintのリスト(昇順用) */
let sortedSprintList = ref();
const selectedSprint = ref("initial");

/* ページ呼び出し時処置 */
onMounted(() => {
  axios
    .get("http://localhost:3000/api/pbls/view_backlog_all/" + id)
    .then((response) => {
      /* 正常取得 */
      if (response.status == 200) {
        awesome2.value = true;

        /* データなし */
        if (response.data.length == 0) {
          awesome.value = false;
        } else {
          /* データがある場合 */
          awesome.value = true;
          PblList.value = response.data;

          for (var i = 0; i < PblList.value.length; i++) {
            idSet.add(String(PblList.value[i].pbl_id));
            // sprintプルダウン用のlist作成
            sprintList.add(PblList.value[i].pbl_sprint);

            // SPが登録されているか否かで条件分岐して登録
            if (PblList.value[i].pbl_sp == null) {
              selectedSp.value.push({
                id: PblList.value[i].id,
                pbl_sp: "SPを選択",
              });
            } else {
              selectedSp.value.push({
                id: PblList.value[i].id,
                pbl_sp: PblList.value[i].pbl_sp,
              });
            }
          }
          // Sprintの昇順ソート
          sortedSprintList = Array.from(sprintList);
          sortedSprintList.sort((a, b) => a - b);

          // sprint値がnullであれば未設定に変更
          for (var i = 0; i < PblList.value.length; i++) {
            if (PblList.value[i].pbl_sprint == null) {
              flag.value = true;
            }
            PblList.value[i].pbl_sprint =
              PblList.value[i].pbl_sprint == null
                ? "未設定"
                : PblList.value[i].pbl_sprint;
          }

          // プルダウンからnullを削除
          sortedSprintList = sortedSprintList.filter((v) => v);
          if (flag.value) {
            sortedSprintList.splice(1, 0, "未設定");
          };

        }
      } else {
      }
    })

    .finally(() => {
      isLoading.value = false;
    });
});

function addPbl() {

  flag.value = false;

  var pblData = {
    pbl_id: PblId.value,
    pbl_name: PblName.value,
    project_id: id,
    pbl_sprint: PblSprint.value,
  };
  // 重複しないID(数値)かつSprintが数値であれば登録
  if (
    !idSet.has(String(PblId.value)) &&
    (!isNaN(PblSprint.value) || PblSprint.value == null) /* && PblName.value.length <= 50 */
  ) {
    axios
      .post(
        "http://localhost:3000/api/pbls/register_backlog",
        JSON.stringify(pblData)
      )
      /* 正しく送信された場合 */
      .then(() => {
        PblList.value.push({ pbl_id: PblId.value, pbl_name: PblName.value });
        idSet.add(String(PblId.value));
        // 入力されたSprintが新規の値であれば追加
        sprintList.add(PblSprint.value);
        // Sprintの昇順ソート
        sortedSprintList = Array.from(sprintList);
        sortedSprintList.sort((a, b) => a - b);
        //nullを削除
        sortedSprintList = sortedSprintList.filter((v) => v);
        awesome.value = true;

        /* 再初期化 */
        selectedSp.value = [];
        flag.value = false

        /* selectedSpを再形成するために必要な処理 */
        axios
          .get("http://localhost:3000/api/pbls/view_backlog_all/" + id)
          .then((response) => {
            /* 正常取得 */
            if (response.status == 200) {
              awesome2.value = true;
              PblList.value = response.data;

              /* データなし */
              if (PblList.value.length == 0) {
                awesome.value = false;
              } else {
                /* データがある場合 */
                awesome.value = true;

                for (var i = 0; i < PblList.value.length; i++) {
                  idSet.add(String(PblList.value[i].pbl_id));
                  // sprintプルダウン用のlist作成
                  sprintList.add(PblList.value[i].pbl_sprint);

                  // SPが登録されているか否かで条件分岐して登録
                  if (PblList.value[i].pbl_sp == null) {
                    selectedSp.value.push({
                      id: PblList.value[i].id,
                      pbl_sp: "SPを選択",
                    });
                  } else {
                    selectedSp.value.push({
                      id: PblList.value[i].id,
                      pbl_sp: PblList.value[i].pbl_sp,
                    });
                  }
                }
                // Sprintの昇順ソート
                sortedSprintList = Array.from(sprintList);
                sortedSprintList.sort((a, b) => a - b);

                // sprint値がnullであれば未設定に変更
                for (var i = 0; i < PblList.value.length; i++) {
                  if (PblList.value[i].pbl_sprint == null) {
                    flag.value = true;
                  }
                  PblList.value[i].pbl_sprint =
                    PblList.value[i].pbl_sprint == null
                      ? "未設定"
                      : PblList.value[i].pbl_sprint;

                }

                // プルダウンからnullを削除

                sortedSprintList = sortedSprintList.filter((v) => v);
                if (flag.value) {
                  sortedSprintList.splice(1, 0, "未設定");

                };

              }
            } else {
              console.log("hello")
            }
          })

          .finally(() => {
            isLoading.value = false;
            console.log(PblList)
          });
      })
      /* エラー時 */
      .catch(() => {
        window.alert(
          "不正な入力です、以下の条件を満たすか確認してください\n\n" +
          "・入力IDが数値であること\n・入力IDがすでに存在するIDと重複していないこと\n・入力Sprintが数値であること"
        );
      })
      /* すべての処理終了後 */
      .finally(() => {
        PblId.value = "";
        PblName.value = "";
        PblSprint.value = null;
      });
  } else {
    window.alert(
      "不正な入力です、以下の条件を満たすか確認してください\n\n" +
      "・入力IDが数値であること\n・入力IDがすでに存在するIDと重複していないこと\n・入力Sprintが数値であること"
    );

    /* 初期化 */
    PblId.value = "";
    PblName.value = "";
    PblSprint.value = null;
  }
  isAddingPbl.value = false;
}

function charLimit(event) {
  if (event.target.value.length > event.target.getAttribute("maxlength")) {
    event.target.blur();
  }
}

function saveSP() {
  for (var i = 0; i < selectedSp.value.length; i++) {
    /* データの形成 */
    const spData = {
      id: String(selectedSp.value[i].id),
      pbl_sp: String(selectedSp.value[i].pbl_sp),
    };

    /* SPが指定された箇所のみ更新 */
    if (!isNaN(selectedSp.value[i].pbl_sp)) {
      axios.post(
        "http://localhost:3000/api/pbls/register_pbl_sp",
        JSON.stringify(spData)
      );

      /* PblListのSPも更新 */
      PblList.value[i].pbl_sp = selectedSp.value[i].pbl_sp;
    }
  }
  /* 画面を元に戻す */
  isEdit.value = false;
}
</script>

<style scoped>
h2 {
  font-size: 24px;
  color: black;
}

.button_container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 10px 0;
}

.buttons {
  width: 120px;
  color: #fff;
  border: 3px solid #fff;
  background: rgba(0, 64, 152, 1);
  border-radius: 8px;
  transition: 0.3s;
  font-size: 14px;
  font-weight: bold;
}

.buttons:hover {
  color: rgba(0, 64, 152, 1);
  background: #fff;
  border: 3px solid rgba(0, 64, 152, 1);
}

.button_pbl {
  margin: 10px auto 0;
}

table {
  margin: 0 auto 80px;
  border-collapse: collapse;
  width: 300px;
  text-align: center;
  box-sizing: border-box;
}

th,
td {
  font-size: 16px;
  text-align: center;
  /* min-width: 130px; */
  padding: 10px;
  height: 60px;
  border: 1px solid black;
}

.edit-sp {
  min-width: 10px;
}

thead {
  background: lightgray;
}

#pbl_id {
  width: 70px;
}

#pbl_name {
  max-width: 100px;
  overflow-wrap: break-word;
}

#pbl_sp {
  min-width: 50px;
  width: 10%;
  max-width: 50px;
}

#edit_sp {
  min-width: 100px;
}

/* pbl入力欄の作成 */

.form_pbl {
  /* height: 10vh; */
  box-sizing: border-box;
  margin-bottom: 10px;
  /* background: orange; */
}

.add_pbl {
  width: 300px;
  display: flex;
  flex-flow: column;
  justify-content: center;
  margin: 5px auto;
}

.input_pbl {
  /* border: 2px solid black; */
  padding-left: 1em;
  border-radius: 8px;
  margin: 0 5px 5px 5px;
  background: rgb(224, 224, 224);
  max-width: 100%;
  height: 3em;
}

::placeholder {
  color: gray;
  /* font-weight: bold; */
}

.back {
  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
}

.select_sprint {
  font-size: 16px;
  padding: 0.4em 0;
  appearance: menulist;
  background: rgb(224, 224, 224);
  border-radius: 8px;
  text-align: center;
  margin-bottom: 10px;
}

@media screen and (min-width: 1000px) {
  .add_pbl {
    width: 400px;
  }

  .input_pbl {
    /* border: 2px solid black; */
    width: 400px;
  }

  table {
    width: 30vw;
  }

  /* #pbl_name {
  max-width: 200px;
  overflow-wrap: break-word;
} */

  .ref_pbl:hover {
    text-decoration: none;
    font-size: 1.3em;
    transition: 0.3s;
  }

  #edit_sp {
    width: 150px;
  }
}
</style>
