from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from os import name, path
from urllib.parse import parse_qs


from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()


class WebServerHandler(BaseHTTPRequestHandler) :
    def do_GET(self):
        if self.path.endswith('/restaurants'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            resturants = session.query(Restaurant).all()
            for res in resturants:
                output += "<h1 style=\"margin:0px;\">%s</h1>" % res.name
                output += "<h1 style=\"margin:0px;\"><a href=%s> Edit </a></h1>" % ("http://localhost:8080/restaurant/{}/edit".format(res.id))
                output += "<h1 style=\"margin:0px;\"><a href=%s> Delete </a></h1>" % ("http://localhost:8080/restaurant/{}/delete".format(res.id))
                output += "<br><br>"
            output += "<h1><a href=%s>Make a New Resturant </h1>" % "http://localhost:8080/restaurants/new"
            output += "</body></html>"
            self.wfile.write(output.encode())
            return

        elif self.path.endswith('/restaurants/new'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Make a New Restaurant</h1>"
            output += '''<form method='POST' action'/new'><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output.encode())
            return

        elif self.path.endswith('/edit'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            id = self.path.split('/')[2]
            res = session.query(Restaurant).filter_by(id = id).one()
            output = ""
            output += "<html><body>"
            output += "<h1>%s</h1>" % res.name
            output += '''<form method='POST' action'/edit'><input name="name" type="text" ><input type="hidden"  name="restId" value="{}"><input type="submit" value="Submit"> </form>'''.format(res.id)
            output += "</body></html>"
            self.wfile.write(output.encode())
            return

        elif self.path.endswith('/delete'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            id = self.path.split('/')[2]
            res = session.query(Restaurant).filter_by(id = id).one()
            output = ""
            output += "<html><body>"
            output += "<h1>Are you sure you want to delete %s</h1>" % res.name
            output += '''<form method='POST' action'/delete'><input type="hidden"  name="restId" value="{}"><input type="submit" value="Submit"> </form>'''.format(res.id)
            output += "</body></html>"
            self.wfile.write(output.encode())
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path.endswith('/new'):
            length = int(self.headers.get('content-length',0))
            data = self.rfile.read(length).decode()
            name = parse_qs(data)['name'][0]
        
            Myres = Restaurant(name=name)
            session.add(Myres)
            session.commit()

        elif self.path.endswith('/edit'):
            length = int(self.headers.get('content-length',0))
            data = self.rfile.read(length).decode()
            name = parse_qs(data)['name'][0]
            restid = parse_qs(data)['restId'][0]

            Myres = session.query(Restaurant).filter_by(id=restid).one()
            Myres.name = name
            session.add(Myres)
            session.commit()
        
        elif self.path.endswith('/delete'):
            length = int(self.headers.get('content-length',0))
            data = self.rfile.read(length).decode()
            restid = parse_qs(data)['restId'][0]

            Myres = session.query(Restaurant).filter_by(id=restid).one()
            session.delete(Myres)
            session.commit()
        
        # length = int(self.headers.get('content-length',0))
        # ctype , pdict = cgi.parse_header(self.headers.get('content-type'))
        # if ctype == "multipart/form-data":
        #     print(self.rfile)
        #     print("XXXXXXXXXXXXXXX")
        #     field = cgi.parse_multipart(self.rfile,pdict)
        #     messagecontent = field.get('message')
        


        self.send_response(303)
        self.send_header('Location','/restaurants')
        self.end_headers()

def main():
    try:
        PORT = 8080
        server = HTTPServer(('',PORT) , WebServerHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == "__main__":
    main()
