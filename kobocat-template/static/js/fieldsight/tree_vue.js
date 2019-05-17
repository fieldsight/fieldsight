// demo data
var data = {
  name: 'My Tree',
  children: [
    { name: 'hello' },
    { name: 'wat' },
    {
      name: 'child folder',
  
      children: [
        {
          name: 'child folder',
      
          children: [
            { name: 'hello' },
            { name: 'wat' }
          ]
        },
        { name: 'hello' },
        { name: 'wat' },
        {
          name: 'child folder',
      
          children: [
            { name: 'hello' },
            { name: 'wat' }
          ]
        }
      ]
    }
  ]
}

// define the item component
Vue.component('item', {
  template: `
    <li>
      <div
        :class="{bold: isFolder}"
        
        @dblclick="changeType">
        <span v-if="isFolder" @click="toggle">[{{ open ? '-' : '+' }}]</span>
        
        <template v-if="isFolder">
        <input type="checkbox" :id="model.name + 'p'" :value="model.name + 'P'" v-model="isChildrenChecked">
        </template>
        <template v-else>
        <input type="checkbox" :id="model.name" :value="model.name" v-model="model.is_checked">
        </template>
        
        <label :for="model.name">{{ model.name }}</label>
        
      </div>
      <ul v-show="open" v-if="isFolder">
        <item
          class="item" 
          v-for="(model, index) in model.children"
          :key="index"
          :model="model">
        </item>
        <li class="add" @click="addChild">+</li>
      </ul>
    </li>`,

  props: {
    model: Object,
  },
  data: function () {
    return {
      open: false,
    }
  },
  computed: {
    isFolder: function () {
      return this.model.children &&
        this.model.children.length
    },

    isChildrenChecked: {
    // getter
    get: function () {
       var checkedobjs = this.model.children.filter(function (el) {
            return "is_checked" in el && el.is_checked === true;
         });
      console.log('herooooo');
      if (checkedobjs){
        console.log("true");
        return true;
      }
              console.log("false");
      return false;

    }
    // setter
   },

    isChildrenCheckeds: {
      get() {

      var checkedobjs = this.model.children.filter(function (el) {
            return "is_checked" in el && el.is_checked === true;
         });
      console.log('herooooo');
      if (checkedobjs){
        console.log("true");
        return true;
      }
              console.log("false");
      return false;

      },

      set(newVal) {
        this.$emit('update:favorite', newVal);
      }
      
    }
    
   
  },
  methods: {
    
    toggle: function () {
      if (this.isFolder) {
        this.open = !this.open
      }
    },
    changeType: function () {
      if (!this.isFolder) {
        Vue.set(this.model, 'children', [])
        this.addChild()
        this.open = true
      }
    },
    addChild: function () {
      this.model.children.push({
        name: 'new stuff'
      })
    }
  }
})

// boot up the demo
var demo = new Vue({
  el: '#tree',
  data: {
    treeData: data
  },
  methods: {
    printdata: function () {
      var self = this;
      console.log(JSON.stringify(this.treeData));
    },
     
  }
})
