<template>
  <main id="main" class="main">
    <div class="pagetitle">
      <div class="col-lg-8">
        <h1><b>FAQ (Часто задаваемые вопросы)</b></h1>
      </div>
    </div>
    <div class="col-10">
      <div class="card info-card sales-card">
        <div class="card-body">
          <!-- Default Accordion -->
          <div v-for="(question, index) in questions" class="accordion" id="accordionExample">
            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                        :data-bs-target="`#collapse${index + 1}`" aria-expanded="false" :aria-controls="`collapse${index + 1}`">
                  <strong>{{question.head}}</strong>
                </button>
              </h2>
              <div :id="`collapse${index + 1}`" class="accordion-collapse collapse" :aria-labelledby="`heading${index + 1}`"
                   data-bs-parent="#accordionExample">
                <div class="accordion-body">
                  {{question.body}}
                </div>
              </div>
            </div>
          </div><!-- End Default Accordion Example -->

        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: "FAQView",
  data: () => ({
    questions: [
      {
        head: 'Что такое MarketData?',
        body: 'Уникальный сервис аналитики. Визуализация и подсчет ключевых показателей. Автоматизированный и системный сервис который выводит ваш бизнес на новый уровень. Это то что вам нужно, даже, если вы только начинаете ваши шаги в продажах.'
      },      {
        head: 'Почему нужна аналитика продаж?',
        body: 'Потому что зная о ваших продажах всё, ваш бизнес сможет вырасти гораздо эффективнее и быстрее.'
      },      {
        head: 'Как приобрести услугу?',
        body: 'Для покупки сервиса связаться с менеджером.'
      },      {
        head: 'Есть ли пробный период?',
        body: 'Нет, но посмотреть как работает услуга, вы можете по запросу. Смотреть контакты. Мы гордимся нашим продуктом и знаем, что результат от пользования сервиса наступает сразу. Чтобы избежать мошенничества, мы не предоставляем пробный период.'
      },      {
        head: 'Как понять какой тариф мне подходит?',
        body: 'Смотреть описание тарифов'
      },      {
        head: 'Я покупаю единоразово или это ежемесячно?',
        body: 'Сервис работает по подписочной системе. Отследить ваш статус можно в личном кабинете.'
      },      {
        head: 'Что будет если я не успею продлить подписку?',
        body: 'Доступ к сервису будет закрыт.'
      },      {
        head: 'Как изменить уровень подписки?',
        body: 'Для изменения уровня подписки необходимо отправить заявку на почту или позвонить по горячей линии.'
      },      {
        head: 'У меня не загружаются отчеты, что делать?',
        body: 'Позвонить в тех поддержку, наша приоритетная задача чтобы ваша аналитика всегда была перед глазами.'
      },      {
        head: 'Оплатил подписку, но не могу получить доступ.',
        body: 'На создание вашего рабочего пространства необходимо время. Подождать от одного двух дней. Если после двух дней нет доступа - позвонить в тех поддержку.'
      },      {
        head: 'Почему нет онлайн оплаты?',
        body: 'Мы хотим чтобы сервис был доступен каждому, поэтому не хотим поднимать цену из-за онлайн оплаты.'
      }
    ]
  })
}
</script>

<style scoped>

</style>