<template>
  <v-container>
    <v-alert
      v-if="newVersion"
      color="green"
      type="success"
      outlined
      v-html="
        $t('settings.new-version-available', {
          aContents:
            'target=\'_blank\' href=\'https://github.com/hay-kot/mealie\' class=\'green--text\'',
        })
      "
    >
    </v-alert>
    <Theme />
    <Backup class="mt-2" />
    <Webhooks class="mt-2" />
    <Migration class="mt-2" />
    <p class="text-center my-2">
      {{ $t("settings.current") }}
      {{ version }} |
      {{ $t("settings.latest") }}
      {{ latestVersion }}
      ·
      <a href="https://hay-kot.github.io/mealie/" target="_blank">
        {{ $t("settings.explore-the-docs") }}
      </a>
      ·
      <a
        href="https://hay-kot.github.io/mealie/contributors/non-coders/"
        target="_blank"
      >
        {{ $t("settings.contribute") }}
      </a>
    </p>
  </v-container>
</template>

<script>
import Backup from "../components/Settings/Backup";
import Webhooks from "../components/Settings/Webhook";
import Theme from "../components/Settings/Theme";
import Migration from "../components/Settings/Migration";
import axios from "axios";

export default {
  components: {
    Backup,
    Webhooks,
    Theme,
    Migration,
  },
  data() {
    return {
      latestVersion: null,
      version: "v0.1.0",
    };
  },
  mounted() {
    this.getVersion();
  },
  computed: {
    newVersion() {
      if ((this.latestVersion != null) & (this.latestVersion != this.version)) {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
    async getVersion() {
      let response = await axios.get(
        "https://api.github.com/repos/hay-kot/mealie/releases/latest"
      );
      this.latestVersion = response.data.tag_name;
    },
  },
};
</script>

<style>
</style>