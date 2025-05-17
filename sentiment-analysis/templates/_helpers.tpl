{{- define "sentiment-chart.fullname" -}}
{{- printf "%s-%s" .Values.prefix .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}