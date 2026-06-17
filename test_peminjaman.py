import psycopg2

conn = psycopg2.connect(dbname='perpus_db', user='postgres', password='farhat09', host='localhost', port='5432')
cur = conn.cursor()

# Check peminjaman table structure
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'peminjaman'
    ORDER BY ordinal_position
""")
print("=== Tabel PEMINJAMAN ===")
rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"  {row[0]}: {row[1]} (nullable: {row[2]})")
else:
    print("  Tabel peminjaman tidak ditemukan!")

# Try test insert
print("\n=== Test Insert ===")
try:
    cur.execute("""
        INSERT INTO peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, petugas, catatan, status)
        VALUES (1, 1, '2026-06-13', '2026-06-20', 'Test', 'S E E M', 'Test note', 'Dipinjam')
    """)
    print("Insert berhasil!")
    conn.rollback()
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    conn.rollback()

cur.close()
conn.close()
