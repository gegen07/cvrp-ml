<template>
  <v-layout class="fill-height">
    <v-row justify="center" no-gutters>
      <v-col cols="6">
        <v-container class="fill-height">
          <v-responsive class="align-center text-justify fill-height">
            <v-row class="d-flex align-center justify-center">
              <v-container class="fill-height">
                <v-container>
                  <p class="text-h2">Como Usar</p>
                </v-container>
                <v-container class="mt-2">
                  <p>Seja bem-vindo ao <b>CVRP-ML</b>! Uma aplicação que aproxima a distância média de vada veículo para o problema do caixeiro viajante com restrições de capacidade. Existe apenas uma maneira de interagir com o serviço web: Pelo botão de "Upload Input", que irá enviar um arquivo de entrada para o serviço web e retornar a distância no card ao lado.</p>
                </v-container>
                <v-container class="mt-2">
                  <p>É esperado que o arquivo de entrada seja um arquivo .json. Para ambos os modos, é esperado que o arquivo de entrada siga o formato de entrada do problema do caixeiro viajante com restrições de capacidade. Para mais informações, acesse a documentação do projeto no GitHub.</p>
                </v-container>
              </v-container>
            </v-row>
          </v-responsive>
        </v-container>
      </v-col>
      <v-col cols="6">
        <v-container class="fill-height">
          <v-responsive class="align-center text-center fill-height">
            <v-row class="d-flex align-center justify-center">
              <v-container class="fill-height">
                <v-container>
                  <p class="text-h4">Resultado</p>
                </v-container>
                <v-container class="mt-2">
                  <p>A distância média percorrida de cada veículo é: {{ distance }} quilômetros</p>
                </v-container>
              </v-container>
            </v-row>
            <v-row class="d-flex align-center justify-center">
              <v-col cols="4">
                  <v-file-input
                    label="Arquivo de Entrada"
                    hide-details="auto"
                    variant="solo-inverted"
                    type="file" id="file_model" ref="file_model"
                    v-on:change="handleFileUpload()"
                    class="mb-0 pb-0"
                  ></v-file-input>
              </v-col>
              <v-col cols="auto">
                <v-btn
                  color="teal"
                  min-width="228"
                  rel="noopener noreferrer"
                  size="x-large"
                  variant="flat"
                  v-on:click="getResult()"
                  class="mt-0 pt-0"
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
        file_model: '',
        distance: 0
      }
    },

    methods: {
      getResult() {
        let formData = new FormData();
            formData.append('file', this.file_model);
            console.log(this.file_model)
            axios.post('http://34.125.189.210:8000/get-distance',
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
        this.file_model = (this.$refs.file_model as any).files[0];
      }
    }
});
</script>
