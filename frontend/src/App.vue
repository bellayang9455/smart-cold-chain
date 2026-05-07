<template>
  <div>
    <nav class="nav">
      <RouterLink to="/">Dashboard</RouterLink>
      <RouterLink to="/boxes">魚貨箱列表</RouterLink>
      <RouterLink to="/alerts">告警紀錄</RouterLink>
    </nav>

    <RouterView />
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: Arial, "Microsoft JhengHei", sans-serif;
  background: #f4f6f8;
}

.nav {
  display: flex;
  gap: 20px;
  padding: 16px 24px;
  background: #1f2937;
}

.nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav a.router-link-active {
  color: #38bdf8;
}
</style>