<template>
  <div id="main">
    <h2 class="title">{{ tierlist_title }}</h2>
    <div id="tier-root">
      <div v-for="(row, index) in tiers" :key="row.id" class="tier-row">
        <div class="tier-label" :style="{ 'background-color': row.color }">
          <div class="label" contenteditable @input="edit($event, index)">
            {{ row.label }}
          </div>
        </div>
        <draggable
          class="tier-sort"
          :list="row.items"
          group="tierlist"
          ghost-class="ghost"
        >
          <div
            v-for="item in row.items"
            :key="item.id"
            class="tier-item"
            :style="{ 'background-image': 'url(' + item.image + ')' }"
          ></div>
        </draggable>
        <div class="tier-config">
          <div class="settings" @click="openOverlay(index)"></div>
          <div class="move-control">
            <div class="move-up" @click="up(index)" v-if="index !== 0"></div>
            <div
              class="move-down"
              @click="down(index)"
              v-if="index !== tiers.length - 1"
            ></div>
          </div>
        </div>
      </div>
    </div>
    <div class="tier-row">
      <draggable
        class="tier-sort"
        :list="items"
        group="tierlist"
        ghost-class="ghost"
      >
        <div
          v-for="item in items"
          :key="item.id"
          class="tier-item"
          :style="{ 'background-image': 'url(' + item.image + ')' }"
        ></div>
      </draggable>
    </div>
    <div id="overlay" :style="config_vis">
      <div class="config">
        <div class="close" @click="closeOverlay()"></div>
        <div
          class="config-banner"
          :style="{ background: tiers[config_row].color }"
        >
          <div class="banner-title">{{ tiers[config_row].label }}</div>
        </div>
        <div class="options">
          <div class="color-select">
            <div
              v-for="color in colors"
              :key="color"
              class="color-icon"
              :style="{ background: color, border: checkColor(color) }"
              @click="changeColor(color)"
            ></div>
          </div>
          <div class="button-group">
            <div class="button" @click="removeRow()">Remove Row</div>
            <div class="button" @click="addRow()">Add Row</div>
          </div>
        </div>
      </div>
    </div>
    <div class="bottom-button-group">
      <input
        type="text"
        class="bottom-button input-box"
        v-model="tierlist_code"
        style="color: #fff"
      />
      <div class="bottom-button" @click="getItems()">Go</div>
      <div class="bottom-button" @click="resetList()">Reset</div>
    </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import axios from 'axios';

export default {
  data() {
    return {
      tiers: [
        { id: 0, label: 'S', color: '#ff7f7f', items: [] },
        { id: 1, label: 'A', color: '#ffbf7f', items: [] },
        { id: 2, label: 'B', color: '#ffdf7f', items: [] },
        { id: 3, label: 'C', color: '#ffff7f', items: [] },
        { id: 4, label: 'D', color: '#bfff7f', items: [] },
      ],
      items: [],
      ntier: 5,
      colors: [
        '#ff7f7f',
        '#ffbf7f',
        '#ffdf7f',
        '#ffff7f',
        '#bfff7f',
        '#7fff7f',
        '#7fffff',
        'R#7fbfff',
        '#7f7fff',
        '#ff7fff',
        '#bf7fbf',
        '#cfcfcf',
      ],
      config_row: 0,
      config_vis: 'visibility: hidden',
      tierlist_code: '',
      tierlist_title: 'Tierlist Title',
    };
  },

  methods: {
    up(index) {
      const temp = this.tiers[index];
      this.$set(this.tiers, index, this.tiers[index - 1]);
      this.$set(this.tiers, index - 1, temp);
    },

    down(index) {
      const temp = this.tiers[index];
      this.$set(this.tiers, index, this.tiers[index + 1]);
      this.$set(this.tiers, index + 1, temp);
    },

    openOverlay(index) {
      this.config_row = index;
      this.config_vis = 'visibility:visible';
    },

    closeOverlay() {
      this.config_vis = 'visibility:hidden';
    },

    edit(e, index = this.config_row) {
      this.tiers[index].label = e.target.textContent;
    },

    checkColor(color) {
      if (this.tiers[this.config_row].color == color) {
        return '2px solid #fff';
      }
    },

    changeColor(color) {
      this.tiers[this.config_row].color = color;
    },

    removeRow() {
      for (var i = 0; i < this.tiers[this.config_row]['items'].length; i++) {
        this.items.push(this.tiers[this.config_row]['items'][i]);
      }
      this.tiers.splice(this.config_row, 1);
      this.closeOverlay();
    },

    addRow() {
      const template = { id: this.ntier, label: 'NEW', color: '', items: [] };
      this.ntier++;
      this.$set(this.tiers, this.tiers.length, template);
      this.config_row = this.tiers.indexOf(template);
      this.openOverlay(this.config_row);
    },

    resetList() {
      for (var i = 0; i < this.tiers.length; i++) {
        for (var j = 0; j < this.tiers[i]['items'].length; j++) {
          console.log(this.tiers[i]['items'][j]);
          this.items.push(this.tiers[i]['items'][j]);
        }
        this.tiers[i]['items'] = [];
      }
    },

    getItems() {
      axios
        .get('http://127.0.0.1:5000/tierlist/' + this.tierlist_code)
        .then((response) => {
          if (response.data == 'invalid code') {
            console.log('invalid code');
          } else {
            this.tierlist_title = response.data.title;
            for (var i = 0; i < response.data.items.length; i++) {
              this.items.push({ id: i, image: response.data.items[i] });
            }
          }
        });
    },
  },

  components: {
    draggable,
  },
};
</script>

<style scoped>
@import '../assets/tierlist.css';
</style>
