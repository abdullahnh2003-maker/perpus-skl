from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.utils.html import escape

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dictfetchone(cursor):
    """Mengubah satu hasil query menjadi dictionary."""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()

    if row is None:
        return None

    return dict(zip(columns, row))

# Dashboard

def dashboard(request):
    total_buku = 0
    total_judul = 0
    sedang_dipinjam = 0
    sudah_dikembalikan = 0
    stok_buku = []
    status_map = {'Dipinjam': 0, 'Dikembalikan': 0}

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(SUM(stok), 0) AS total_buku FROM buku")
            result = dictfetchone(cursor)
            total_buku = result['total_buku'] if result else 0

            cursor.execute("SELECT COUNT(*) AS total_judul FROM buku")
            result = dictfetchone(cursor)
            total_judul = result['total_judul'] if result else 0

            cursor.execute("SELECT COUNT(*) AS total FROM peminjaman WHERE status = 'Dipinjam'")
            result = dictfetchone(cursor)
            sedang_dipinjam = result['total'] if result else 0
            status_map['Dipinjam'] = sedang_dipinjam

            cursor.execute("SELECT COUNT(*) AS total FROM peminjaman WHERE status = 'Kembali'")
            result = dictfetchone(cursor)
            sudah_dikembalikan = result['total'] if result else 0
            status_map['Dikembalikan'] = sudah_dikembalikan

            cursor.execute("SELECT judul, COALESCE(stok, 0) AS stok FROM buku ORDER BY stok DESC, judul ASC LIMIT 10")
            stok_buku = dictfetchall(cursor)
    except Exception:
        total_buku = 0
        total_judul = 0
        sedang_dipinjam = 0
        sudah_dikembalikan = 0
        stok_buku = []
        status_map = {'Dipinjam': 0, 'Dikembalikan': 0}

    return render(request, 'dashboard.html', {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'stok_buku': stok_buku,
        'status_map': status_map,
    })


def buku_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM buku
            ORDER BY id ASC
        """)
        buku = dictfetchall(cursor)

    return render(request, 'buku/list.html', {
        'buku': buku
    })


# CREATE

def buku_create(request):
    if request.method == 'POST':

        judul = request.POST['judul']
        pengarang = request.POST['pengarang']
        kategori = request.POST['kategori']
        penerbit = request.POST['penerbit']
        tahun_terbit = request.POST['tahun_terbit']
        rak = request.POST['rak']
        stok = request.POST['stok']
        deskripsi = request.POST['deskripsi']

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO buku (
                    judul,
                    pengarang,
                    kategori,
                    penerbit,
                    tahun_terbit,
                    rak,
                    stok,
                    deskripsi
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, [
                judul,
                pengarang,
                kategori,
                penerbit,
                tahun_terbit,
                rak,
                stok,
                deskripsi
            ])

        return redirect('buku_list')

    return render(request, 'buku/create.html')


# DETAIL

def buku_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                id,
                judul,
                pengarang,
                kategori,
                penerbit,
                tahun_terbit,
                rak,
                stok,
                deskripsi
            FROM buku
            WHERE id = %s
        """, [id])
    
        buku = dictfetchone(cursor)
    
    return render(request, 'buku/detail.html', {
        'buku': buku
    })


# UPDATE

def buku_update(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM buku
            WHERE id = %s
        """, [id])

        buku = dictfetchone(cursor)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE buku
                SET
                    judul=%s,
                    pengarang=%s,
                    kategori=%s,
                    penerbit=%s,
                    tahun_terbit=%s,
                    rak=%s,
                    stok=%s,
                    deskripsi=%s
                WHERE id=%s
            """, [
                request.POST['judul'],
                request.POST['pengarang'],
                request.POST['kategori'],
                request.POST['penerbit'],
                request.POST['tahun_terbit'],
                request.POST['rak'],
                request.POST['stok'],
                request.POST['deskripsi'],
                id
            ])

        return redirect('buku_list')

    return render(request, 'buku/update.html', {
        'buku': buku
    })

# DELETE

def buku_delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM buku
            WHERE id = %s
        """, [id])

        buku = dictfetchone(cursor)

    if request.method == 'POST':

        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM buku
                WHERE id = %s
            """, [id])

        return redirect('buku_list')

    return render(request, 'buku/delete.html', {
        'buku': buku
    })


# ---- Siswa CRUD (raw SQL style, mirrors buku handlers)

def siswa_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nama, kelas, nis, is_active
            FROM siswa
            ORDER BY id ASC
        """)
        siswa = dictfetchall(cursor)

    return render(request, 'siswa/list.html', {
        'siswa': siswa
    })


def siswa_create(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        nis = request.POST.get('nis')
        kelas = request.POST.get('kelas')
        is_active = request.POST.get('is_active') == 'on'

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO siswa (
                    nama, nis, kelas, is_active
                ) VALUES (%s,%s,%s,%s)
            """, [nama, nis, kelas, is_active])

        return redirect('siswa_list')

    return render(request, 'siswa/create.html')


def siswa_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nama, kelas, nis, is_active FROM siswa WHERE id = %s
        """, [id])
        siswa = dictfetchone(cursor)
        
        if siswa:
            try:
                # Total peminjaman siswa ini
                cursor.execute("SELECT COUNT(*) as total FROM peminjaman WHERE siswa_id = %s", [id])
                total_peminjaman = dictfetchone(cursor)
                siswa['total_peminjaman'] = total_peminjaman['total'] if total_peminjaman else 0

                # Peminjaman aktif (belum dikembalikan)
                cursor.execute("SELECT COUNT(*) as total FROM peminjaman WHERE siswa_id = %s AND status = 'Dipinjam'", [id])
                peminjaman_aktif = dictfetchone(cursor)
                siswa['peminjaman_aktif'] = peminjaman_aktif['total'] if peminjaman_aktif else 0
            except Exception:
                # Jika tabel peminjaman belum ada
                siswa['total_peminjaman'] = 0
                siswa['peminjaman_aktif'] = 0

    return render(request, 'siswa/detail.html', {'siswa': siswa})


def siswa_update(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nama, kelas, nis, is_active FROM siswa WHERE id = %s
        """, [id])
        siswa = dictfetchone(cursor)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE siswa SET
                    nama=%s,
                    nis=%s,
                    kelas=%s,
                    is_active=%s
                WHERE id=%s
            """, [
                request.POST.get('nama'),
                request.POST.get('nis'),
                request.POST.get('kelas'),
                # Menerima nilai pilihan '1' atau '0' (string) atau nilai truthy lainnya untuk checkbox
                True if str(request.POST.get('is_active')).strip() in ['1', 'true', 'True', 'on', 't'] else False,
                id
            ])

        return redirect('siswa_list')

    return render(request, 'siswa/update.html', {'siswa': siswa})


def siswa_delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nama, kelas, nis, is_active FROM siswa WHERE id = %s
        """, [id])
        siswa = dictfetchone(cursor)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM siswa WHERE id = %s
            """, [id])

        return redirect('siswa_list')

    return render(request, 'siswa/delete.html', {'siswa': siswa})


def peminjaman_list(request):
    peminjaman = []
    error_message = None

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    p.id,
                    COALESCE(s.nama, '-') AS siswa,
                    COALESCE(b.judul, '-') AS buku,
                    p.tanggal_pinjam,
                    p.jatuh_tempo,
                    p.keperluan,
                    'D O U L' AS petugas,
                    p.status
                FROM peminjaman p
                LEFT JOIN siswa s ON s.id = p.siswa_id
                LEFT JOIN buku b ON b.id = p.buku_id
                ORDER BY p.id ASC
            """)
            peminjaman = dictfetchall(cursor)
    except Exception:
        error_message = 'Tabel peminjaman belum tersedia atau kolomnya belum lengkap.'

    return render(request, 'peminjaman/list.html', {
        'peminjaman': peminjaman,
        'error_message': error_message,
    })


def peminjaman_create(request):
    siswa_list = []
    buku_list = []
    error_message = None

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nama FROM siswa ORDER BY nama ASC")
            siswa_list = dictfetchall(cursor)
            cursor.execute("SELECT id, judul, stok FROM buku ORDER BY judul ASC")
            buku_list = dictfetchall(cursor)
    except Exception:
        error_message = 'Tabel siswa atau buku belum tersedia.'

    if request.method == 'POST':
        try:
            siswa_id = request.POST.get('siswa_id')
            buku_id = request.POST.get('buku_id')
            tanggal_pinjam = request.POST.get('tanggal_pinjam')
            jatuh_tempo = request.POST.get('jatuh_tempo')
            keperluan = request.POST.get('keperluan')
            status = 'Dipinjam'

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO peminjaman (
                        siswa_id, buku_id, tanggal_pinjam, jatuh_tempo,
                        keperluan, status
                    ) VALUES (%s,%s,%s,%s,%s,%s)
                """, [
                    siswa_id, buku_id, tanggal_pinjam, jatuh_tempo,
                    keperluan, status
                ])

            return redirect('peminjaman_list')
        except Exception as e:
            error_message = f'Gagal menyimpan data peminjaman: {str(e)}'

    return render(request, 'peminjaman/create.html', {
        'siswa_list': siswa_list,
        'buku_list': buku_list,
        'error_message': error_message,
    })


def peminjaman_return(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE peminjaman
                    SET status = 'Kembali'
                    WHERE id = %s
                """, [id])
        except Exception:
            pass

    return redirect('peminjaman_list')
