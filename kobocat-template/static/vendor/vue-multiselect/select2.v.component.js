
Vue.component('select2', {
  props: {
    options: {
      type: [Object, Array]
    },
    value: {
      type: [Array,Number, String]
    },
    multiple: {
      type: Boolean,
      default:false
    }
  },
  // props: ['options', 'value', 'multiple'],
  template:
  `<select>
    <slot></slot>
  </select>`,
  mounted: function () {
    var vm = this
    $(this.$el)
      // .select2({ data: this.options })
      .select2({ data: this.select2Options })
      .val(this.value)
      .trigger('change')
      // emit event on change.
      .on('change', function () {
        vm.$emit('input', this.value)
      })
  },
  computed: {
    select2Options(){
      return this.options.map(o=>{
        o.text = o.name;
        return o;
      })
    }
  },
  watch: {
    value: function (value) {
      // update value
      $(this.$el).val(value).trigger('change');
    },
    options: function (options) {
      // update options
      $(this.$el).select2({ data: options })
    }
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
});


