{{- define "sentiment-chart.fullname" -}}
{{- printf "%s-%s" .Values.prefix .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "sentiment.name" -}}
sentiment
{{- end }}

{{- define "sentiment.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name "sentiment" | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}