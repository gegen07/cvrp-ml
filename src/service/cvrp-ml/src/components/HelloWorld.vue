<template>
  <v-layout class="fill-height">
    <v-row justify="center" no-gutters>
      <v-col cols="6">
        <v-container class="fill-height">
          <v-responsive class="align-center text-justify fill-height">
            <v-row class="d-flex align-center justify-center">
              <v-card class="align-center" width="400">
                <v-card-item>
                  <v-card-title>Como Usar</v-card-title>
                </v-card-item>

                <v-card-text>
                  Seja bem-vindo ao CVRP-ML! Uma aplicação que aproxima a distância média de vada veículo para o problema do caixeiro viajante com restrições de capacidade. Existem duas maneiras de interagir com o serviço web: (1) Pelo botão de "Retrain Model", que irá re-treinar o modelo de aprendizado de máquina com os dados de entrada mais os dados que já estão no servidor e (2) Pelo botão de "Upload Input", que irá enviar um arquivo de entrada para o serviço web e retornar a distância no card ao lado.

                  Para o primeiro modo, é esperado que o arquivo de entrada seja um arquivo zip contendo vários arquivos .json. Para o segundo modo, é esperado que o arquivo de entrada seja um arquivo .json. Para ambos os modos, é esperado que o arquivo de entrada siga o formato de entrada do problema do caixeiro viajante com restrições de capacidade. Para mais informações, acesse a documentação do projeto no GitHub.
                </v-card-text>
              </v-card>
            </v-row>
            <v-row class="d-flex align-center justify-center">
              <v-col cols="auto">
                  <v-text-field
                    label="Arquivo de Entrada"
                    hide-details="auto"
                    type="file" id="files" ref="files"
                    v-on:change="handleFileUpload()"
                  ></v-text-field>
              </v-col>
              <v-col cols="auto">
                <v-btn
                  color="primary"
                  min-width="228"
                  rel="noopener noreferrer"
                  size="x-large"
                  variant="flat"
                  v-on:click="submitFile()"
                >
                  <v-icon
                    icon="mdi-zip-box"
                    size="large"
                    start
                  />

                  Retreinar Modelo
                </v-btn>
              </v-col>
            </v-row>
          </v-responsive>
        </v-container>
      </v-col>
      <v-col cols="6">
        <v-container class="fill-height">
          <v-responsive class="align-center text-center fill-height">
            <v-row class="d-flex align-center justify-center">
              <v-card class="align-center" width="400">
                <v-card-item>
                  <v-card-title>Resultado</v-card-title>
                </v-card-item>

                <v-card-text>
                  A distância média percorrida para cada veículo é: {{ distance }}
                </v-card-text>
              </v-card>
            </v-row>
            <v-row class="d-flex align-center justify-center">
              <v-col cols="auto">
                  <v-text-field
                    label="Arquivo de Entrada"
                    hide-details="auto"
                    type="file" id="file_model" ref="file_model"
                    v-on:change="handleFileUpload()"
                  ></v-text-field>
              </v-col>
              <v-col cols="auto">
                <v-btn
                  color="primary"
                  min-width="228"
                  rel="noopener noreferrer"
                  size="x-large"
                  variant="flat"
                  v-on:click="getResult()"
                >
                  <v-icon
                    icon="mdi-file-arrow-up-down-outline"
                    size="large"
                    start
                  />

                  Executar Modelo
                </v-btn>
              </v-col>
            </v-row>
          </v-responsive>
        </v-container>
      </v-col>
    </v-row>

  </v-layout>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent } from 'vue';
export default defineComponent({
    data(){
      return {
        file: '',
        file_model: '',
        distance: 0
      }
    },

    methods: {
      submitFile(){
            let formData = new FormData();
            formData.append('file', this.file);
            console.log(this.file)
            axios.post('/retrain-model',
                formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
              }
            ).then(function(){
          console.log('SUCCESS!!');
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      },

      getResult() {
        let formData = new FormData();
            formData.append('file', this.file_model);
            console.log(this.file_model)
            axios.post('http://localhost:8000/get-distance',
                formData,
                {
                headers: {
                  'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
                  'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
                  'Content-Type': 'multipart/form-data'
                }
              }
            ).then(response => this.distance = response.data.distance)
        .catch(function(){
          console.log('FAILURE!!');
        });
      },

      handleFileUpload(){
        this.file = this.$refs.files.files[0];
        this.file_model = this.$refs.file_model.files[0];
      }
    }
});
</script>
