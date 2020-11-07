from backend import app, db
from backend.utils import sanitizeString
from backend.models import Disciplinas, Users, Mamao, Penoso, Gostei, NaoGostei, Comentario, Links
from backend.views import DisciplinasInformacoes, ComentariosInformacoes, LinksInformacoes, AvaliacoesDisciplinas, AvaliacoesComentario
    
from passlib.hash import sha256_crypt


def getDisciplinas():
    return getDisciplina()


def getDisciplina(id_disciplina=None):
    if id_disciplina:
        disciplina = DisciplinasInformacoes.query.filter_by(id=id_disciplina).first()
        if disciplina:
            value = disciplina.serialize()
        else:
            value = {}
    else:
        disciplinas = Disciplinas.query.all()
        sort_disciplinas = sorted(
            [d.serialize() for d in disciplinas], 
            key=lambda x: x['nome']
        )
        value = sort_disciplinas
    return value


def cadastroUsuario(data):
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    picture = data.get('picture', '')
    password = sha256_crypt.encrypt(str(data.get('password')))

    r = Users.query.filter_by(username=username).first()
    if r:
        return False, 'Username já cadastrado'
    r = Users.query.filter_by(email=email).first()
    if r:
        return False, 'Email já cadastrado'

    novo_usuario = Users(name=name, email=email, username=username, picture=picture, password=password)
    db.session.add(novo_usuario)
    db.session.commit()
    return True, None


def checkUsuario(username, passwordEntered):
    r = Users.query.filter_by(username=username).first()

    if r:
        correctPassword = r.password
        # compare hash with entered hash
        if sha256_crypt.verify(passwordEntered, correctPassword):
            data = r.serialize()
            data['password'] = ''
            return True, data

    return False, None


def cadastroAvaliacaoDisciplina(categoria, id_disciplina, id_user):
    try:
        id_user = int(id_user)
        r = AvaliacoesDisciplinas.query.filter_by(id_disciplina=id_disciplina, id_user=id_user).first()
        if r:
            return False, 'Voce ja avaliou essa disciplina'

        if categoria == 'mamao':
            nova_avaliacao = Mamao(id_disciplina=id_disciplina, id_user=id_user)
        else:
            nova_avaliacao = Penoso(id_disciplina=id_disciplina, id_user=id_user)
        
        db.session.add(nova_avaliacao)
        db.session.commit()
        return True, None

    except Exception as e:
        print(e)
        return False, "Um ocorreu enquanto processava"

    
def cadastroAvaliacaoComentario(id_comentario, categoria, id_user):
    try:
        id_user = int(id_user)
        r = AvaliacoesComentario.query.filter_by(id_comentario=id_comentario, id_user=id_user).first()
        if r:
            return False, 'Voce ja avaliou esse comentario'

        if categoria == 'gostei':
            nova_avaliacao = Gostei(id_comentario=id_comentario, id_user=id_user)
        else:
            nova_avaliacao = NaoGostei(id_comentario=id_comentario, id_user=id_user)
        
        db.session.add(nova_avaliacao)
        db.session.commit()
        return True, None

    except Exception as e:
        print(e)
        return False, "ocorreu um erro enquanto processava"
    

def cadastroDisciplina(nome, penoso_mamao, id_user):
    try:
        nome_limpo = ' '.join([sanitizeString(x) for x in nome.split(' ')])
        id_user = int(id_user)

        r = Disciplinas.query.filter_by(nome_limpo=nome_limpo).first()
        if r:
            return False, 'Disciplina ja cadastrada'

        nova_disciplina = Disciplinas(id_user=id_user, nome=nome, nome_limpo=nome_limpo)
        db.session.add(nova_disciplina)
        db.session.commit()
        return cadastroAvaliacaoDisciplina(penoso_mamao, nova_disciplina.id, id_user)

    except Exception as e:
        print(e)
        return False, "ocorreu um erro enquanto processava"


def cadastroComentario(id_user, id_disciplina, texto):
    try:
        id_user = int(id_user)
        novo_comentario = Comentario(id_user=id_user, id_disciplina=id_disciplina, texto=texto)
        db.session.add(novo_comentario)
        db.session.commit()
        return True, None

    except Exception as e:
        print(e)
        return False, "ocorreu um erro enquanto processava"


def cadastroLink(id_user, id_disciplina, titulo, link):
    try:
        id_user = int(id_user)
        novo_link = Links(id_user=id_user, id_disciplina=id_disciplina, titulo=titulo, link=link)
        db.session.add(novo_link)
        db.session.commit()
        return True, None

    except Exception as e:
        print(e)
        return False, "ocorreu um erro enquanto processava"


def getComentarios(id_disciplina=None):
    if id_disciplina:
        comentarios = ComentariosInformacoes.query.filter_by(id_disciplina=id_disciplina).all()
    else:
        comentarios = ComentariosInformacoes.query.all()

    if comentarios:
        sort_comentarios = sorted(
            [c.serialize() for c in comentarios], 
            key=lambda x: x['id_comentario']
        )
        value = sort_comentarios
    else:
        value = comentarios

    return value


def getLinks(id_disciplina=None):
    if id_disciplina:
        links = LinksInformacoes.query.filter_by(id_disciplina=id_disciplina).all()
    else:
        links = ComentariosInformacoes.query.all()

    if links:
        sort_links = sorted(
            [l.serialize() for l in links], 
            key=lambda x: x['id_link']
        )
        value = sort_links
    else:
        value = links

    return value


def getTopDisciplinas(n, categoria):
    TIPOS = ['mamao', 'penoso']

    disciplinas = DisciplinasInformacoes.query.all()
    disciplinas = [d.serialize() for d in disciplinas]
    
    if categoria not in TIPOS:
        return {}

    for disciplina in disciplinas:
        disciplina['razao'] = disciplina['num_mamao']/(disciplina['num_mamao']+disciplina['num_penoso'])
        disciplina['num_votos'] = disciplina['num_mamao']+disciplina['num_penoso']

    reverse = True if categoria == 'mamao' else False

    sort_disciplinas = sorted(disciplinas, key=lambda x: x['razao'], reverse=reverse)

    size = min(n, len(sort_disciplinas))

    return sort_disciplinas[:size]
