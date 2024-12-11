#!/bin/bash

# Variabel untuk konfigurasi
ZONE_NAME="bakso"
DOMAIN_NAME="$1"
RECORD_TYPE="A"
IP_ADDRESS="34.101.57.163"
TTL=300


# Validasi apakah DOMAIN_NAME sudah diatur
if [ -z "$DOMAIN_NAME" ]; then
  echo "Error: DOMAIN belum diset. Jalankan skrip dengan format:"
  echo "  sh deployment/gcp/development.sh stg-srvc-\${PROJECT_NAME}-ext.bakso.my.id."
  exit 1
fi

# Fungsi untuk mengecek apakah domain memiliki record aktif
check_domain_active() {
  gcloud dns record-sets list --zone="$ZONE_NAME" --name="$DOMAIN_NAME" --type="$RECORD_TYPE" --format="value(name)" | grep -q "$DOMAIN_NAME"
}

# Mengecek domain
if check_domain_active; then
  echo "Domain $DOMAIN_NAME sudah aktif. Tidak ada tindakan yang diperlukan."
else
  echo "Domain $DOMAIN_NAME tidak ditemukan. Menambahkan record baru..."

  # Memulai transaksi
  gcloud dns record-sets transaction start --zone="$ZONE_NAME"

  # Menambahkan record baru
  gcloud dns record-sets transaction add --zone="$ZONE_NAME" \
      --name="$DOMAIN_NAME" \
      --type="$RECORD_TYPE" \
      --ttl="$TTL" \
      "$IP_ADDRESS"

  # Menyelesaikan transaksi
  gcloud dns record-sets transaction execute --zone="$ZONE_NAME"

  echo "Record $DOMAIN_NAME berhasil ditambahkan."
fi
