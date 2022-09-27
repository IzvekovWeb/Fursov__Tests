<template>
  <div class="dialog" v-if="show" @click.stop="hideDialog">
    <div @click.stop class="dialog_content">
      <form>
        <div class="row mb-3">
          <label for="ordersAmount" class="col-md-4 col-lg-3 col-form-label">Заказы шт</label>
          <div class="col-md-8 col-lg-9">
            <input v-model="plan.orders_count" name="ordersAmount" type="number" class="form-control" id="ordersAmount">
          </div>
        </div>

        <div class="row mb-3">
          <label for="ordersRub" class="col-md-4 col-lg-3 col-form-label">Заказы руб</label>
          <div class="col-md-8 col-lg-9">
            <input v-model="plan.orders_rub" name="ordersRub" type="number" class="form-control" id="ordersRub">
          </div>
        </div>
        <div class="row mb-3">
          <label for="SoldAmount" class="col-md-4 col-lg-3 col-form-label">Выкупы шт</label>
          <div class="col-md-8 col-lg-9">
            <input v-model="plan.sold_count" name="SoldAmount" type="number" class="form-control" id="SoldAmount">
          </div>
        </div>
        <div class="row mb-3">
          <label for="SoldRub" class="col-md-4 col-lg-3 col-form-label">Выкупы руб</label>
          <div class="col-md-8 col-lg-9">
            <input v-model="plan.sold_rub" name="SoldRub" type="number" class="form-control" id="SoldRub">
          </div>
        </div>
        <div class="row mb-3">
          <label for="Delivery" class="col-md-4 col-lg-3 col-form-label">Логистика</label>
          <div class="col-md-8 col-lg-9">
            <input v-model="plan.logistic" name="Delivery" type="number" class="form-control" id="Delivery">
          </div>
        </div>
        <div class="row mb-3">
          <label for="Realizing" class="col-md-4 col-lg-3 col-form-label">К перечислению</label>
          <div class="col-md-8 col-lg-9">
            <input v-model="plan.realize" name="Realizing" type="number" class="form-control" id="Realizing">
          </div>
        </div>
        <div class="row mb-3">
          <label for="PercentBuyback" class="col-md-4 col-lg-3 col-form-label">Процент выкупа</label>
          <div class="col-md-8 col-lg-9">
            <input v-model="plan.sell_percent" name="PercentBuyback" type="number" class="form-control"
                   id="PercentBuyback">
          </div>
        </div>

        <div class="text-center">
          <button type="submit" class="btn btn-primary" @click.prevent="submitDialog">Изменить</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import API_URL from "@/consts";
import api from "@/api";

export default {
  name: "PlanModal",
  props: {
    show: {
      type: Boolean,
      default: false
    },
    url: {
      type: String
    }
  },
  data: () => ({
    plan: {
      orders_rub: '',
      orders_count: '',
      sold_rub: '',
      sold_count: '',
      logistic: '',
      realize: '',
      sell_percent: ''
    }
  }),
  methods: {
    hideDialog() {
      this.$emit('update:show', false)
    },
    submitDialog() {
      if (this.plan.sell_percent && this.plan.realize && this.plan.orders_rub && this.plan.orders_count && this.plan.sold_count && this.plan.sold_rub && this.plan.logistic) {
        return api
            .put(API_URL + this.url, this.plan)
            .then(response => {
              this.hideDialog()
            })
            .catch(error => {});
      }
      if (!this.plan.sell_percent) document.getElementById('PercentBuyback').classList.add('danger-input')
      if (!this.plan.sold_rub) document.getElementById('SoldRub').classList.add('danger-input')
      if (!this.plan.sold_count) document.getElementById('SoldAmount').classList.add('danger-input')
      if (!this.plan.orders_count) document.getElementById('ordersAmount').classList.add('danger-input')
      if (!this.plan.orders_rub) document.getElementById('ordersRub').classList.add('danger-input')
      if (!this.plan.realize) document.getElementById('Realizing').classList.add('danger-input')
      if (!this.plan.logistic) document.getElementById('Delivery').classList.add('danger-input')
    }
  }
}
</script>

<style scoped>
.dialog {
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  display: flex;
  z-index: 9999;
}

.dialog_content {
  min-width: 500px;
  padding: 25px;
  margin: auto;
  background: #fff;
  border-radius: 12px;
  min-height: 50px;
}

.danger-input {
  border: 2px solid red ;
}

.form-control:focus {
  border: 2px solid blue ;
}
</style>