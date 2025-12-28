<template>
  <div class="container">
    <h2>Create Assignment Rule Set</h2>

    <!-- Assignment Info -->
    <h3>Assignment Info</h3>
    <input v-model="subject" placeholder="Subject Name" />
    <input v-model="experiment" placeholder="Experiment / Assignment Title" />
    <input v-model="experimentNo" placeholder="Experiment Number" />

    <hr />

    <!-- Aim -->
    <label>
      <input type="checkbox" v-model="rules.aim.required" />
      Aim Section Required
    </label>

    <!-- Theory -->
    <label>
      <input type="checkbox" v-model="rules.theory.required" />
      Theory Section Required
    </label>
    <div v-if="rules.theory.required">
      Min Words:
      <input type="number" v-model.number="rules.theory.min_words" />
      Max Words:
      <input type="number" v-model.number="rules.theory.max_words" />
    </div>

    <!-- Code -->
    <label>
      <input type="checkbox" v-model="rules.code.required" />
      Code Section Required
    </label>
    <div v-if="rules.code.required">
      <label>
        <input type="checkbox" v-model="rules.code.check_comments" />
        Check Comments
      </label>
      <label>
        <input type="checkbox" v-model="rules.code.check_indentation" />
        Check Indentation
      </label>
    </div>

    <!-- Output -->
    <label>
      <input type="checkbox" v-model="rules.output.required" />
      Output Section Required
    </label>
    <div v-if="rules.output.required">
      <select v-model="rules.output.type">
        <option value="image">Image</option>
        <option value="text">Text</option>
        <option value="image_or_text">Image or Text</option>
      </select>
    </div>

    <!-- Methodology -->
    <label>
      <input type="checkbox" v-model="rules.methodology.required" />
      Methodology Required
    </label>
    <div v-if="rules.methodology.required">
      <label>
        <input type="checkbox" value="image" v-model="rules.methodology.formats" />
        Handwritten Image
      </label>
      <label>
        <input type="checkbox" value="text" v-model="rules.methodology.formats" />
        Text Explanation
      </label>
    </div>

    <!-- Conclusion -->
    <label>
      <input type="checkbox" v-model="rules.conclusion.required" />
      Conclusion Required
    </label>
    <div v-if="rules.conclusion.required">
      Min Words:
      <input type="number" v-model.number="rules.conclusion.min_words" />
      Max Words:
      <input type="number" v-model.number="rules.conclusion.max_words" />
    </div>

    <!-- Plagiarism -->
    <h3>Plagiarism</h3>
    Allowed Similarity (%):
    <input type="number" v-model.number="rules.plagiarism_threshold" />

    <br /><br />
<button @click="saveRules">Save Assignment</button>
<button @click="$emit('close')">Cancel</button>

<pre v-if="generatedRules">{{ generatedRules }}</pre>


    <!-- JSON Output -->
    <pre v-if="generatedRules">{{ generatedRules }}</pre>
  </div>
</template>

<script>
export default {
  name: "TeacherRuleBuilder",
  data() {
    return {
      subject: "",
      experiment: "",
      experimentNo: "",
      rules: {
        student_details: true,
        aim: { required: true },
        theory: { required: false, min_words: 300, max_words: 600 },
        code: { required: false, check_comments: true, check_indentation: true },
        output: { required: false, type: "image_or_text" },
        methodology: { required: false, formats: [] },
        conclusion: { required: false, min_words: 100, max_words: 200 },
        plagiarism_threshold: 25
      },
      generatedRules: null
    };
  },
 methods: {
  generateRules() {
    const ruleSet = {
      subject: this.subject,
      experiment: this.experiment,
      experiment_no: this.experimentNo,
      ...this.rules
    };

    this.generatedRules = JSON.stringify(ruleSet, null, 2);
    return ruleSet;
  },

  saveRules() {
    const ruleSet = this.generateRules();
    this.$emit("save", ruleSet);
  }
}

};
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
}
input,
select {
  margin: 5px;
}
pre {
  background: #f5f5f5;
  padding: 10px;
}
</style>
