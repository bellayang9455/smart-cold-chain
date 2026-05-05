<template>
  <div>
    <header class="topbar">
      <h2>智慧冷鏈監控系統</h2>

      <nav>
        <RouterLink to="/">首頁</RouterLink>
        <RouterLink to="/fish">魚貨列表</RouterLink>
        <RouterLink to="/alerts">告警紀錄</RouterLink>
      </nav>
    </header>

    <RouterView />
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: Arial, "Microsoft JhengHei", sans-serif;
  background: #f4f6f8;
}

.topbar {
  background: #0f172a;
  color: white;
  padding: 16px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.topbar h2 {
  margin: 0;
}

nav {
  display: flex;
  gap: 20px;
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

nav a.router-link-active {
  color: #38bdf8;
}
</style>