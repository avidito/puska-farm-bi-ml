PGDMP         0                {            puska_dwh_dummy    15.3    15.3 %    ,           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            -           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            .           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            /           1262    17685    puska_dwh_dummy    DATABASE     q   CREATE DATABASE puska_dwh_dummy WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE puska_dwh_dummy;
                postgres    false            �            1259    17694 
   dim_lokasi    TABLE     �   CREATE TABLE public.dim_lokasi (
    id bigint NOT NULL,
    provinsi character varying(100),
    kabupaten_kota character varying(100),
    created_dt timestamp without time zone,
    modified_dt timestamp without time zone
);
    DROP TABLE public.dim_lokasi;
       public         heap    postgres    false            �            1259    17693    dim_lokasi_id_seq    SEQUENCE     z   CREATE SEQUENCE public.dim_lokasi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.dim_lokasi_id_seq;
       public          postgres    false    217            0           0    0    dim_lokasi_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.dim_lokasi_id_seq OWNED BY public.dim_lokasi.id;
          public          postgres    false    216            �            1259    17701    dim_unit_ternak    TABLE       CREATE TABLE public.dim_unit_ternak (
    id bigint NOT NULL,
    id_lokasi bigint,
    nama_unit character varying(100),
    longitude numeric(12,10),
    latitude numeric(12,10),
    created_dt timestamp without time zone,
    modified_dt timestamp without time zone
);
 #   DROP TABLE public.dim_unit_ternak;
       public         heap    postgres    false            �            1259    17700    dim_unit_ternak_id_seq    SEQUENCE        CREATE SEQUENCE public.dim_unit_ternak_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.dim_unit_ternak_id_seq;
       public          postgres    false    219            1           0    0    dim_unit_ternak_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.dim_unit_ternak_id_seq OWNED BY public.dim_unit_ternak.id;
          public          postgres    false    218            �            1259    17687 	   dim_waktu    TABLE     �   CREATE TABLE public.dim_waktu (
    id bigint NOT NULL,
    tahun bigint,
    bulan bigint,
    minggu bigint,
    tanggal bigint,
    created_dt timestamp without time zone,
    modified_dt timestamp without time zone
);
    DROP TABLE public.dim_waktu;
       public         heap    postgres    false            �            1259    17686    dim_waktu_id_seq    SEQUENCE     y   CREATE SEQUENCE public.dim_waktu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.dim_waktu_id_seq;
       public          postgres    false    215            2           0    0    dim_waktu_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.dim_waktu_id_seq OWNED BY public.dim_waktu.id;
          public          postgres    false    214            �            1259    17733    fact_produksi    TABLE     H  CREATE TABLE public.fact_produksi (
    id_waktu bigint NOT NULL,
    id_lokasi bigint NOT NULL,
    id_unit_ternak bigint NOT NULL,
    id_jenis_produk bigint NOT NULL,
    id_sumber_pasokan bigint NOT NULL,
    jumlah_produksi bigint,
    created_dt timestamp without time zone,
    modified_dt timestamp without time zone
);
 !   DROP TABLE public.fact_produksi;
       public         heap    postgres    false            �            1259    17713 	   pred_susu    TABLE     �   CREATE TABLE public.pred_susu (
    id integer NOT NULL,
    id_waktu bigint,
    id_lokasi bigint,
    id_unit_ternak bigint,
    prediction numeric(10,2)
);
    DROP TABLE public.pred_susu;
       public         heap    postgres    false            �            1259    17712    your_table_name_id_seq    SEQUENCE        CREATE SEQUENCE public.your_table_name_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.your_table_name_id_seq;
       public          postgres    false            �           2604    17697    dim_lokasi id    DEFAULT     n   ALTER TABLE ONLY public.dim_lokasi ALTER COLUMN id SET DEFAULT nextval('public.dim_lokasi_id_seq'::regclass);
 <   ALTER TABLE public.dim_lokasi ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216    217            �           2604    17704    dim_unit_ternak id    DEFAULT     x   ALTER TABLE ONLY public.dim_unit_ternak ALTER COLUMN id SET DEFAULT nextval('public.dim_unit_ternak_id_seq'::regclass);
 A   ALTER TABLE public.dim_unit_ternak ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    219    219            �           2604    17690    dim_waktu id    DEFAULT     l   ALTER TABLE ONLY public.dim_waktu ALTER COLUMN id SET DEFAULT nextval('public.dim_waktu_id_seq'::regclass);
 ;   ALTER TABLE public.dim_waktu ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    214    215    215            $          0    17694 
   dim_lokasi 
   TABLE DATA           [   COPY public.dim_lokasi (id, provinsi, kabupaten_kota, created_dt, modified_dt) FROM stdin;
    public          postgres    false    217   W,       &          0    17701    dim_unit_ternak 
   TABLE DATA           q   COPY public.dim_unit_ternak (id, id_lokasi, nama_unit, longitude, latitude, created_dt, modified_dt) FROM stdin;
    public          postgres    false    219   �,       "          0    17687 	   dim_waktu 
   TABLE DATA           _   COPY public.dim_waktu (id, tahun, bulan, minggu, tanggal, created_dt, modified_dt) FROM stdin;
    public          postgres    false    215   �,       )          0    17733    fact_produksi 
   TABLE DATA           �   COPY public.fact_produksi (id_waktu, id_lokasi, id_unit_ternak, id_jenis_produk, id_sumber_pasokan, jumlah_produksi, created_dt, modified_dt) FROM stdin;
    public          postgres    false    222   ,-       (          0    17713 	   pred_susu 
   TABLE DATA           X   COPY public.pred_susu (id, id_waktu, id_lokasi, id_unit_ternak, prediction) FROM stdin;
    public          postgres    false    221   �-       3           0    0    dim_lokasi_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.dim_lokasi_id_seq', 1, false);
          public          postgres    false    216            4           0    0    dim_unit_ternak_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.dim_unit_ternak_id_seq', 1, false);
          public          postgres    false    218            5           0    0    dim_waktu_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.dim_waktu_id_seq', 1, false);
          public          postgres    false    214            6           0    0    your_table_name_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.your_table_name_id_seq', 1, false);
          public          postgres    false    220            �           2606    17699    dim_lokasi dim_lokasi_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.dim_lokasi
    ADD CONSTRAINT dim_lokasi_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.dim_lokasi DROP CONSTRAINT dim_lokasi_pkey;
       public            postgres    false    217            �           2606    17706 $   dim_unit_ternak dim_unit_ternak_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.dim_unit_ternak
    ADD CONSTRAINT dim_unit_ternak_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.dim_unit_ternak DROP CONSTRAINT dim_unit_ternak_pkey;
       public            postgres    false    219            �           2606    17692    dim_waktu dim_waktu_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.dim_waktu
    ADD CONSTRAINT dim_waktu_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.dim_waktu DROP CONSTRAINT dim_waktu_pkey;
       public            postgres    false    215            �           2606    17737     fact_produksi fact_produksi_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.fact_produksi
    ADD CONSTRAINT fact_produksi_pkey PRIMARY KEY (id_waktu, id_lokasi, id_unit_ternak, id_jenis_produk, id_sumber_pasokan);
 J   ALTER TABLE ONLY public.fact_produksi DROP CONSTRAINT fact_produksi_pkey;
       public            postgres    false    222    222    222    222    222            �           2606    17717    pred_susu pred_susu_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.pred_susu
    ADD CONSTRAINT pred_susu_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.pred_susu DROP CONSTRAINT pred_susu_pkey;
       public            postgres    false    221            �           2606    17707 .   dim_unit_ternak dim_unit_ternak_id_lokasi_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_unit_ternak
    ADD CONSTRAINT dim_unit_ternak_id_lokasi_fkey FOREIGN KEY (id_lokasi) REFERENCES public.dim_lokasi(id);
 X   ALTER TABLE ONLY public.dim_unit_ternak DROP CONSTRAINT dim_unit_ternak_id_lokasi_fkey;
       public          postgres    false    3464    217    219            �           2606    17723 "   pred_susu pred_susu_id_lokasi_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.pred_susu
    ADD CONSTRAINT pred_susu_id_lokasi_fkey FOREIGN KEY (id_lokasi) REFERENCES public.dim_lokasi(id);
 L   ALTER TABLE ONLY public.pred_susu DROP CONSTRAINT pred_susu_id_lokasi_fkey;
       public          postgres    false    3464    221    217            �           2606    17728 '   pred_susu pred_susu_id_unit_ternak_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.pred_susu
    ADD CONSTRAINT pred_susu_id_unit_ternak_fkey FOREIGN KEY (id_unit_ternak) REFERENCES public.dim_unit_ternak(id);
 Q   ALTER TABLE ONLY public.pred_susu DROP CONSTRAINT pred_susu_id_unit_ternak_fkey;
       public          postgres    false    3466    219    221            �           2606    17718 !   pred_susu pred_susu_id_waktu_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.pred_susu
    ADD CONSTRAINT pred_susu_id_waktu_fkey FOREIGN KEY (id_waktu) REFERENCES public.dim_waktu(id);
 K   ALTER TABLE ONLY public.pred_susu DROP CONSTRAINT pred_susu_id_waktu_fkey;
       public          postgres    false    221    215    3462            $   1   x�3��J,OT(��--�,(�O����KO���".Cdi�H4F��� 0TD      &   5   x�3�4�̫�PHK,��44�3�4^�q��A���0¢>F��� Vp�      "   ?   x�Mȱ�0�Y>��e'����;�A� NLp��D��=�,�R�g+��Vϣ�Q�'">���      )   S   x�e��	�0��<L��8ޢd�9�P9�:��0(�0�'b$Oj�3��z� ER���`+���^tR�ǤQ_�ok"r��$�      (   O   x�-�� 1Cѳ)&g�e��cb��'��@�����RE���Ю���S�ϑ��*M�ΐVV�vV���bK_1����     