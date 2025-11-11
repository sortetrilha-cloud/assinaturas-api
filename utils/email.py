def enviar_email_loteria(cliente, jogos, loteria, produto):
    service = autenticar_gmail()

    # Normaliza o nome da loteria e pega cores da config
    loteria_key = loteria.lower().replace(' ', '')
    config = LOTERIAS_CONFIG.get(loteria_key, LOTERIAS_CONFIG['megasena'])

    cor_titulo = config['cor']
    coluna_coringa = config['coluna']

    # Gera HTML da tabela
    stats = jogos.to_html(index=False, justify='center', classes='tabela-jogos')

    # Destaca coluna do coringa se existir
    if coluna_coringa and f"<th>{coluna_coringa}</th>" in stats:
        stats = stats.replace(
            f'<th>{coluna_coringa}</th>',
            f'<th style="color: orange; font-weight: bold;">CORINGA</th>'
        )
        stats = stats.replace(coluna_coringa, '<span style="color: orange; font-weight:bold;">CORINGA</span>')

    # Caminho do anexo
    caminho_anexo = fr"C:\Users\Weskley\Documents\Automatizador de Código\{loteria}.txt"

    # HTML estilizado e responsivo
    corpo_html = f'''
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f9f9f9;
          color: #333;
          padding: 20px;
          margin: 0;
        }}
        .container {{
          background: white;
          border-radius: 10px;
          box-shadow: 0 4px 10px rgba(0,0,0,0.1);
          padding: 20px;
          max-width: 800px;
          margin: auto;
        }}
        h1 {{
          color: {cor_titulo};
          text-align: center;
        }}
        .link {{
          color: #1a73e8;
          font-weight: bold;
          text-decoration: none;
        }}

        /* 🔥 Container da tabela com barra de rolagem no topo */
        .tabela-wrapper {{
          position: relative;
          margin-top: 15px;
        }}

        /* Barra de rolagem no topo */
        .scroll-top {{
          overflow-x: auto;
          overflow-y: hidden;
          height: 20px;
          scrollbar-color: {cor_titulo} #f1f1f1;
          scrollbar-width: thin;

          /* rolagem suave e responsiva */
          -webkit-overflow-scrolling: touch;
          scroll-behavior: smooth;
        }}

        .scroll-top::-webkit-scrollbar {{
          height: 10px;
        }}
        .scroll-top::-webkit-scrollbar-track {{
          background: #f1f1f1;
          border-radius: 10px;
        }}
        .scroll-top::-webkit-scrollbar-thumb {{
          background-color: {cor_titulo};
          border-radius: 10px;
          border: 2px solid #f1f1f1;
        }}
        .scroll-top::-webkit-scrollbar-thumb:hover {{
          background-color: #333;
        }}

        /* Área da tabela principal */
        .tabela-container {{
          overflow-x: auto;
          overflow-y: hidden;
          border: 3px solid {cor_titulo};
          border-radius: 8px;
          padding: 5px;
          margin-top: 5px;
          scrollbar-color: {cor_titulo} #f1f1f1;
          scrollbar-width: thin;

          /* Sincroniza com o topo */
          -webkit-overflow-scrolling: touch;
          scroll-behavior: smooth;
        }}

        /* Tabela estilizada */
        table {{
          border-collapse: collapse;
          width: 100%;
          min-width: 1200px; /* 🔥 aumenta a sensibilidade da rolagem */
        }}
        th, td {{
          border: 1px solid #ddd;
          padding: 8px;
          text-align: center;
          font-size: 14px;
        }}
        th {{
          background-color: {cor_titulo};
          color: white;
          position: sticky;
          top: 0;
          z-index: 1;
        }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #e9f5ff; }}
        .footer {{
          text-align: center;
          margin-top: 20px;
          font-size: 14px;
          color: #666;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>{produto}</h1>
        <p style="font-size: 18px; text-align:center;">🎥 PARA ENTENDER NOSSO E-MAIL, ASSISTA O VÍDEO ABAIXO:</p>
        <p style="text-align:center;"><a href="https://youtu.be/DucRbPk4tQM?si=5delHAiFu0qdKf3i" class="link">👉 LINK DO VÍDEO</a></p>

        <h2 style="text-align:center; color:{cor_titulo};">AQUI ESTÁ SEU JOGO COM O CORINGA!</h2>

        <div class="tabela-wrapper">
          <div class="scroll-top" id="scrollTop"></div>  <!-- Barra de rolagem no topo -->
          <div class="tabela-container" id="scrollTable">
            {stats}
          </div>
        </div>

        <p style="font-size: 18px; text-align:center; margin-top: 20px;">📱 Caso a tabela não apareça corretamente, veja este vídeo:</p>
        <p style="text-align:center;"><a href="https://youtu.be/0Ijqjp8tSkI" class="link">LINK DO VÍDEO DE SUPORTE</a></p>

        <div class="footer">
          <p>🍀 Boa sorte!<br><b>Sistema Automático | Sorte Trilha</b></p>
          <img src="cid:einstein_cid" style="width:100px; margin-top:10px;">
        </div>
      </div>

      <!-- Sincroniza o scroll do topo com a tabela -->
      <script>
        const topScroll = document.getElementById('scrollTop');
        const tableScroll = document.getElementById('scrollTable');
        topScroll.addEventListener('scroll', () => {{
          tableScroll.scrollLeft = topScroll.scrollLeft;
        }});
        tableScroll.addEventListener('scroll', () => {{
          topScroll.scrollLeft = tableScroll.scrollLeft;
        }});
      </script>
    </body>
    </html>
    '''



    # Criação da mensagem
    mensagem = MIMEMultipart("related")
    mensagem["to"] = cliente
    mensagem["subject"] = "🎲 SEUS JOGOS PARA O PRÓXIMO CONCURSO!!!"
    alternativa = MIMEMultipart("alternative")
    mensagem.attach(alternativa)
    alternativa.attach(MIMEText(corpo_html, "html"))

    # Anexa imagem padrão
    with open(IMAGEM_PADRAO, 'rb') as img:
        imagem = MIMEImage(img.read())
        imagem.add_header('Content-ID', '<einstein_cid>')
        mensagem.attach(imagem)

    # Anexa arquivo TXT
    if os.path.exists(caminho_anexo):
        with open(caminho_anexo, "rb") as anexo:
            parte = MIMEBase("application", "octet-stream")
            parte.set_payload(anexo.read())
            encoders.encode_base64(parte)
            parte.add_header("Content-Disposition", f"attachment; filename={os.path.basename(caminho_anexo)}")
            mensagem.attach(parte)

    # Envio via Gmail API
    raw_message = base64.urlsafe_b64encode(mensagem.as_bytes()).decode()
    message = {'raw': raw_message}
    enviado = service.users().messages().send(userId="me", body=message).execute()
