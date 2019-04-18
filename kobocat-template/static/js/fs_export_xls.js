Vue.component('checkbox-item', {
  template: `<label class="checkbox-item">
                <input type="checkbox" :checked="value"
                       @change="$emit('input', $event.target.checked)"
                       class="checkbox-input">
                <span class="checkbox-label">
                  <slot></slot>
                </span>
              </label>
            `,
  props: ['value']
})

new Vue({
  el: '#generateXls',
  data: {
    // This will toggle into true/false   
    checkData: null
  }
})