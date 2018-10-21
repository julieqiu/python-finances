{% extends "base.html" %}

{% block content %}

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
