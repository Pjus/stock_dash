{% extends "mail_templated/base.tpl" %}
{% load static %}
{% load dash_filter %}

{% block subject %}
Recommandation
{% endblock %}

{% block html %}
<div class="card-body p-3">
    <table class="table align-items-center mb-0">
        <thead>
          <tr>
            <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Ticker</th>
            <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Sector</th>
            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Current Price</th>
            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Target Price</th>
            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Register Date</th>

          </tr>
        </thead>
        <tbody>
            {% for mail in mail_ticker %}
            <tr>
                <td>
                  <div class="d-flex px-2 py-1">
                    <div class="d-flex flex-column justify-content-center">
                      <!--  -->
                      <p class="text-xs text-secondary mb-0 text-uppercase stock-long-name">{{mail.company.company_name}}</p>
                    </div>
                  </div>
                </td>
                <td>
                    <h6 class="mb-0 text-sm text-uppercase">{{mail.company.sector}}</h6>
                    <p class="text-xs font-weight-bold mb-0">{{mail.company.industry}}</p>
                </td>
                <td>
                    <p class="text-xs text-center font-weight-bold mb-0">$ {{mail.company.last_price|rounded}}</p>
                </td>
                <td>
                    <p class="text-xs text-center font-weight-bold mb-0 stock-target-price">$ {{mail.company.target_mean_price}}</p>
                </td>

                <td class="align-middle text-center text-sm">
                {% if mail.company.recommandation == 'buy' %}
                  <span class="badge badge-sm bg-gradient-success">{{mail.company.recommandation}}</span>
                {% else %}
                  <span class="badge badge-sm bg-gradient-warning">{{mail.company.recommandation}}</span>
                {% endif %}
                
                </td>
                <td class="align-middle text-center">
                  <span class="text-secondary text-xs font-weight-bold">{{mail.create_date|date:"Y-m-d"}}</span>
                </td>
              </tr>
            {% endfor %}
        </tbody>
      </table>
</div>
{% endblock %}


