# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:50:18 2020

@author: tadeumansi
"""
import zipfile
import io

class EditM:
    def __init__(self, pbit_atual, pbit_novo, codigo_velho, codigo_novo ):
        self.pbit_atual = pbit_atual
        self.pbit_novo = pbit_novo
        self.codigo_velho = codigo_velho
        self.codigo_novo = codigo_novo
        atual_zip = zipfile.ZipFile(pbit_atual,mode='r')
        atual_lista_arquivo = atual_zip.filelist
        novo_zipfile = zipfile.ZipFile(pbit_novo,mode='w',compression=zipfile.ZIP_DEFLATED)
        for al in atual_lista_arquivo:
            if al.filename == 'DataMashup':
                with atual_zip.open(al.filename,'r') as datamashup_byte_stream:
                    revisado_DataMashup = edit_Section(codigo_velho,codigo_novo,datamashup_byte_stream)
                    revisado_DataMashup.seek(0)
                    final_DataMashup = revisado_DataMashup.read()
                    novo_zipfile.writestr('DataMashup',data=final_DataMashup)
            else:
                with atual_zip.open(al,'r') as temp_f:
                    temp_bytes = temp_f.read()
                novo_zipfile.writestr(al,data=temp_bytes)
        print("Modificações no código M realizadas com Sucesso !!!")        
        atual_zip.close()
        novo_zipfile.close()
        
                                
def edit_Section(texto_velho,novo_texto,datamashup_byte_stream):
    byte_dict = {}
    
    with datamashup_byte_stream as f:
        f.seek(0)
        byte_dict['version'] = f.read(4)
        byte_dict['pkg_parts_len'] = f.read(4)
        byte_dict['pkg_parts'] = f.read(int.from_bytes(byte_dict['pkg_parts_len'],byteorder='little'))
        byte_dict['perm_len'] = f.read(4)
        byte_dict['perm_var'] = f.read(int.from_bytes(byte_dict['perm_len'],byteorder='little'))
        byte_dict['meta_len'] = f.read(4)
        byte_dict['meta_var'] = f.read(int.from_bytes(byte_dict['meta_len'],byteorder='little'))
        byte_dict['perm_bind_len'] = f.read(4)
        byte_dict['perm_bind_var'] = f.read(int.from_bytes(byte_dict['perm_bind_len'],byteorder='little'))
        mashup_f = io.BytesIO(byte_dict['pkg_parts'] )
        mashup_zip = zipfile.ZipFile(mashup_f,mode='r')
        conteudo_arquivo = mashup_zip.filelist
        '''
        Abre os arquivos compactados do arquivo mashup, dentro da pasta /Formulas/ o arquivo Section1.m 
        contem todos códigos M do nosso arquivo pbit.        
        '''
        with mashup_zip.open('Formulas/Section1.m','r') as section1_f:
            section1_texto = section1_f.read()
            section1_novo = section1_texto.replace(texto_velho,novo_texto)
        
        #Cria um novo arquivo zip na memoria
        zip_buffer = io.BytesIO()
        zip_archive = zipfile.ZipFile(zip_buffer,mode='w',compression=zipfile.ZIP_DEFLATED)
        #o loop e uma lista dos arquivos compactados do arquivo mashup
        for ac in conteudo_arquivo:
            #se for o arquivo Section1.m abra ele e escreva o novo conteudo
            if ac.filename == 'Formulas/Section1.m':
                zip_archive.writestr('Formulas/Section1.m',data=section1_novo)
                zip_archive.extractall()
            else: 
                with mashup_zip.open(ac,'r') as temp_f:
                    temp_bytes = temp_f.read()
                zip_archive.writestr(ac,data=temp_bytes)
        
        #fecha os streams
        zip_archive.close()
        mashup_zip.close()
        
        zip_buffer.seek(0)
        byte_dict['pkg_parts'] = zip_buffer.read()  
        byte_dict['pkg_parts_len'] = len(byte_dict['pkg_parts']).to_bytes(4,byteorder='little')
        f.close()
        
    new_mashup = io.BytesIO()
    #cria um novo arquivo DataMashup com nossas alteracoes
    for b in ['version','pkg_parts_len','pkg_parts','perm_len','perm_var','meta_len','meta_var','perm_bind_len','perm_bind_var']:
        new_mashup.write(byte_dict[b])
    
    return new_mashup


pbit_antigo = r"f1_antigo.pbit"
pbit_novo = r"f1_novo.pbit"
codigo_velho = bytes('Table.TransformColumnTypes(Data10,{{"Fabricante", type text}, {"Fabricante2", type text}, {"País", type text}, {"Total", Int64.Type}, {"Temporadas", type text}})','utf-8')
codigo_novo = bytes('Table.TransformColumnTypes(Data10,{{"Fabricante", type text}, {"Fabricante2", type text}, {"Total", Int64.Type}, {"Temporadas", type text}})','utf-8')
m = EditM(pbit_antigo,pbit_novo,codigo_velho,codigo_novo)       

                
                
                