<template>
  <div class="page-wrapper">
    <div class="header">
      <iconBtn><img src="../../public/assets/icon/icon-arrow-black.svg"></img></iconBtn>
      <h1>Бронирование</h1>
    </div>
    <div class="main">

    </div>
    <div class="search">
        <NInput placeholder="Поиск"></NInput>
        <ul>
          <addressSelect></addressSelect>
          <addressSelect></addressSelect>
          <addressSelect></addressSelect>
          <addressSelect></addressSelect>

        </ul>
    </div>
    <div  class="booking">
      <NButton type="primary"><p>Забронировать</p></NButton>
    </div>
  </div>
</template>

<script setup>
import iconBtn from '@/components/ui/icon-btn.vue';
import { NInput } from 'naive-ui';
import addressSelect from '@/components/shared/addressSelect.vue';
import { NButton } from 'naive-ui';
</script>

<style scoped>
.booking {
  display: flex;
  justify-content: center;
}
.page-wrapper {
  display: flex;
  flex-direction: column;
  gap: 27px;
}
ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-top: 20px;
}

.search {
  padding-top: 20px;
  border-radius: 50%;
}

.main {
  background-image: url('../../public/assets/icon/map.PNG');
  padding-bottom: 400px;
}

.header {
  display: flex;
  flex-direction: row;
  text-align: center;
}
.header button {
  padding-top: 15px;
}
h1 {
  width: 100%;

}
</style>


