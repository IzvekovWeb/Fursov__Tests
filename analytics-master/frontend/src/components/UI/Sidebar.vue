<template>
  <!-- ======= Sidebar ======= -->
  <aside id="sidebar" class="sidebar">
    <ul class="sidebar-nav" id="sidebar-nav">
      <li class="nav-item">
        <router-link class="nav-link collapsed" to="/">
          <i class="bi bi-grid"></i>
          <span>Главная</span>
        </router-link>
      </li> <!-- Дашборд -->
      <li class="nav-item">
        <router-link class="nav-link collapsed" to="/profile">
          <i class="bi bi-person"></i>
          <span>Профиль</span>
        </router-link>
      </li> <!--  Профиль  -->
      <li class="nav-item">
        <a class="nav-link collapsed" data-bs-target="#icons-nav" data-bs-toggle="collapse" href="#">
          <i class="bi bi-menu-button-wide"></i><span>Аналитика</span><i class="bi bi-chevron-down ms-auto"></i>
        </a>
        <ul id="icons-nav" class="nav-content collapse" data-bs-parent="#sidebar-nav">
          <li>
            <router-link class="no-decor" to="/analytic/wildberries">
              <i class="bi bi-circle"></i><span>Wildberries</span>
            </router-link>
          </li>
        </ul>
        <ul id="icons-nav" class="nav-content collapse" data-bs-parent="#sidebar-nav">
          <li>
            <router-link class="no-decor" to="/analytic/selfsell">
              <i class="bi bi-circle"></i><span>Выкупы</span>
            </router-link>
          </li>
        </ul>
      </li> <!-- Аналитика -->

      <li class="nav-item">
        <router-link class="nav-link collapsed" to="/faq">
          <i class="bi bi-question-circle"></i>
          <span>F.A.Q</span>
        </router-link>
      </li><!-- F.A.Q -->
      <li class="nav-item">
        <router-link class="nav-link collapsed" to="/tariffs">
          <i class="bi bi-credit-card-2-front"></i>
          <span>Тарифы</span>
        </router-link>
      </li><!-- Тарифы -->
      <li class="nav-item">
        <router-link class="nav-link collapsed" to="/contacts">
          <i class="bi bi-envelope"></i>
          <span>Обратная связь</span>
        </router-link>
      </li><!-- Контакты -->
    </ul>
  </aside>
</template>

<script>
export default {
  name: "Sidebar",
  methods: {
    changeBodyClass() {
      var bodyClass = document.body.classList
      if (!bodyClass.length) {
        document.body.classList.add('toggle-sidebar')
      } else {
        document.body.classList.remove('toggle-sidebar')
      }

    }
  },
}
</script>

<style>
.no-decor {
  text-decoration: none;
}
</style>