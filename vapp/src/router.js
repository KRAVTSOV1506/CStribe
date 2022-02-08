import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      component: () => import("./views/Index"),
      children: [
        {
          path: "",
          component: () => import("./views/Home"),
        },
      ],
    },
    {
      path: "*",
      component: () => import("./views/Index"),
      children: [
        {
          name: "404",
          path: "",
          component: () => import("./views/404"),
        },
      ],
    },
  ],
});
