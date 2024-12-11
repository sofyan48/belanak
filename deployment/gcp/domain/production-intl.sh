#!/bin/bash

# Variabel untuk konfigurasi
ZONE_NAME="internal-kiriminaja"
DOMAIN_NAME="prd-belanak-intl.kiriminaja.io"
RECORD_TYPE="A"
IP_ADDRESS="10.184.0.69"
TTL=300

# Jika argumen kedua adalah "false", keluar tanpa error
if [ "$2" = "false" ]; then
  echo "Service is not internal"
  exit 0
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
