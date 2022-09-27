<template>
  <main id="main" class="main">

    <section class="section profile" v-if="!loading">
      <div class="row">
        <div class="col-xl-4">

          <div class="card">
            <div class="card-body profile-card pt-4 d-flex flex-column align-items-center">

              <img src="@/assets/user.png" alt="Profile" class="rounded-circle">
              <h2>{{ USER.full_name }}</h2>
              <h3>{{ USER.tariff }}</h3>

            </div>
          </div>

        </div>

        <div class="col-xl-8">

          <div class="card">
            <div class="card-body pt-3">
              <!-- Bordered Tabs -->
              <ul class="nav nav-tabs nav-tabs-bordered">

                <li class="nav-item">
                  <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#profile-overview">Общие</button>
                </li>

                <li class="nav-item">
                  <button class="nav-link" data-bs-toggle="tab" data-bs-target="#profile-edit">Токены</button>
                </li>

                <!--                <li class="nav-item">-->
                <!--                  <button class="nav-link" data-bs-toggle="tab" data-bs-target="#profile-change-password">Смена пароля-->
                <!--                  </button>-->
                <!--                </li>-->

              </ul>
              <div class="tab-content pt-2">

                <div class="tab-pane fade show active profile-overview" id="profile-overview">
                  <div class="row">
                    <div class="col-lg-3 col-md-4 label">Полное имя</div>
                    <div class="col-lg-9 col-md-8">{{ USER.full_name }}</div>
                  </div>

                  <div class="row">
                    <div class="col-lg-3 col-md-4 label">Телефон</div>
                    <div class="col-lg-9 col-md-8">{{ USER.phone_num }}</div>
                  </div>

                  <div class="row">
                    <div class="col-lg-3 col-md-4 label">Почта</div>
                    <div class="col-lg-9 col-md-8">{{ USER.email }}</div>
                  </div>

                  <div class="row">
                    <div class="col-lg-3 col-md-4 label">Тариф</div>
                    <div class="col-lg-9 col-md-8">{{ USER.tariff }}</div>
                  </div>

                  <div class="row">
                    <div class="col-lg-3 col-md-4 label">Дата подключения</div>
                    <div class="col-lg-9 col-md-8">{{ USER.date_follow }}</div>
                  </div>
                  <div class="row">
                    <div class="col-lg-3 col-md-4 label">Действителен до</div>
                    <div class="col-lg-9 col-md-8">{{ USER.date_expire }}</div>
                  </div>


                </div>

                <div class="tab-pane fade profile-edit pt-3" id="profile-edit">
                    <token-form :suppliers="SUPPLIERS_WITHOUT_TOKENS"/>
                </div>

                <!--                <div class="tab-pane fade pt-3" id="profile-change-password">-->
                <!--                  &lt;!&ndash; Change Password Form &ndash;&gt;-->
                <!--                  <form>-->

                <!--                    <div class="row mb-3">-->
                <!--                      <label for="currentPassword" class="col-lg-3 col-md-4 label">Старый пароль</label>-->
                <!--                      <div class="col-md-8 col-lg-9">-->
                <!--                        <input name="password" type="password" class="form-control" id="currentPassword">-->
                <!--                      </div>-->
                <!--                    </div>-->

                <!--                    <div class="row mb-3">-->
                <!--                      <label for="newPassword" class="col-lg-3 col-md-4 label">Новый пароль</label>-->
                <!--                      <div class="col-md-8 col-lg-9">-->
                <!--                        <input name="newpassword" type="password" class="form-control" id="newPassword">-->
                <!--                      </div>-->
                <!--                    </div>-->

                <!--                    <div class="row mb-3">-->
                <!--                      <label for="renewPassword" class="col-lg-3 col-md-4 label">Повторый ввод</label>-->
                <!--                      <div class="col-md-8 col-lg-9">-->
                <!--                        <input name="renewpassword" type="password" class="form-control" id="renewPassword">-->
                <!--                      </div>-->
                <!--                    </div>-->

                <!--                    <div class="text-center">-->
                <!--                      <button type="submit" class="btn btn-primary">Изменить</button>-->
                <!--                    </div>-->
                <!--                  </form>&lt;!&ndash; End Change Password Form &ndash;&gt;-->

                <!--                </div>-->

              </div><!-- End Bordered Tabs -->

            </div>
          </div>

        </div>
      </div>
    </section>

  </main>
</template>

<script>
import {mapGetters} from "vuex";
import baseMixin from "@/mixins/baseMixin";
import tokenForm from "@/components/forms/TokenForm";

export default {
  name: "ProfileView",
  components: {
    tokenForm
  },

  computed: mapGetters(['USER', 'SUPPLIERS_WITHOUT_TOKENS']),
  mixins: [baseMixin],
  async mounted() {
    await this.$store.dispatch('GET_USER')
    await this.$store.dispatch('GET_SUPPLIERS_WITHOUT_TOKENS')
    this.loading = false
  }
}
</script>

<style scoped>

</style>