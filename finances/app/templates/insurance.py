{% extends "base.html" %}

{% block content %}
<style>

.header {
  background: cornflowerblue;
  color: white;
  font-size: 16px;
  font-weight: bold;
  text-transform: uppercase;
}

.green {
  color: darkgreen;
}

.red {
  color: red;
}

.gray {
  color: gray;
}

.font-size-16 {
  font-size: 16px;
}

.font-size-20 {
  font-size: 20px;
}

.font-size-24 {
  font-size: 24px;
}

h2 {
  font-size: 24px;
}

table {
  font-size: 18px;
  margin: 10px 0;
}

td {
  padding-right: 5px;
  font-family: helvetica;
  font-size: 14px;
  text-transform: uppercase;
}


form {
  font-size: 18px;
}

.card {
  width: 45%;
  min-height: 200px;
  background: lavender;
  display: inline-block;
  vertical-align: top;
  margin: 10px;
  padding: 10px;
}

.month {
    font-size: 48px;
    text-transform: uppercase;
    font-weight: 600;
    color: #2196F3;
}

p.summary {
    font-size: 24px;
    display: inline-flex;
    margin-right: 10px;
    margin-bottom: 0;
    padding: 2px;
    background: white;
}

h2.l1 {
    font-weight: 500;
    font-size: 32px;
}

h2.l2 {
    font-weight: 500;
    margin: 0;
}

h2.l3 {
    font-weight: 100;
    margin-bottom: 0;
    text-transform: uppercase;
    margin-top: 20px;
    font-size: 18px;
}

.group {
    background: white;
    padding: 10px 20px;
    margin: 20px 0;
}

</style>
{% for claim in insurance_claims.items() %}
<div class="card overview">
  {% for report in report_dict.reports %}
    {% if report and report.data %}
    <div class="group">
      <h2 class="l1">
        <span>{{ report.header }}: </span>
        <span>{{ report.data.total }}</span>
      </h2>

      {% for l2, l2_report in report.data.categories.items() %}

        {% if l2_report.name == "Expenses" %}
          <h2 class="l2">{{ l2 }}: {{ l2_report.total }} </h2>
        {% endif %}

        {% for l3, l3_report in l2_report.categories.items() %}
          {% if l2.name != "Other" and l2.name != "Skipped" %}
            <h2 class="l3">{{ l3 }}: {{ l3_report.total }} </h2>
          {% endif %}

          <table>
          {% for t in l3_report.transactions %}
            <tr>
              <td>{{ t.date.month }}/{{ t.date.day }}/{{ t.date.year }}</td>
              <td>{{ t.description }}</td>
              <td>{{ t.amount }}</td>
            </tr>
          {% endfor %}
          </table>

        {% endfor %}
      {% endfor %}
    </div>
    {% endif %}
  {% endfor %}
</div>
{% endfor %}

{% endblock %}
