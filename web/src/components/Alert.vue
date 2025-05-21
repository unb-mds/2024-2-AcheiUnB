<template>
  <div
    v-if="visible"
    :class="[
      'fixed right-4 top-16 px-4 py-3 rounded flex items-center justify-between font-inter',
      alertClasses[type],
      'z-[10001]'
    ]"
    role="alert"
  >
    <p>{{ message }}</p>
    <button
      @click="closeAlert"
      :class="['ml-4 font-bold focus:outline-none', alertClassesText[type]]"
    >
      ✕
    </button>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      default: "info",
      validator: (value) => ["success", "error", "info", "warning"].includes(value),
    },
    message: {
      type: String,
      required: true,
    },
    duration: {
      type: Number,
      default: 3000,
    },
  },
  data() {
    return {
      visible: true,
    };
  },
  computed: {
    alertClasses() {
      return {
        success: "bg-green-200 border-r-4 border-green-600 text-green-600",
        error: "bg-red-200 border-r-4 border-red-600 text-red-600",
        info: "bg-blue-500",
        warning: "bg-yellow-500 text-black",
      };
    },
    alertClassesText() {
      return {
        success: "text-green-600",
        error: "text-red-600",
        info: "text-blue-600",
        warning: "text-black-600",
      };
    },
  },
  mounted() {
    if (this.duration > 0) {
      setTimeout(() => {
        this.closeAlert();
      }, this.duration);
    }
  },
  methods: {
    closeAlert() {
      this.visible = false;
      this.$emit("closed");
    },
  },
};
</script>
