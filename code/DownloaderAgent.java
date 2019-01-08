
package MultiAgentSystems;

import jade.core.Agent;
import jade.core.behaviours.OneShotBehaviour;
import jade.core.behaviours.FSMBehaviour;
import jade.core.behaviours.CyclicBehaviour;

import jade.lang.acl.*;

import scraper.aux;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

public class DownloaderAgent extends Agent
{
    String search;

    private class Scraping extends FSMBehaviour
    {
        String scrapped_content = " ";
        private class InformManager extends OneShotBehaviour
        {
            public void action()
            {
                System.out.printf("Agent %s is requiring job\n", myAgent.getName());
                
                ACLMessage request_message = new ACLMessage(ACLMessage.REQUEST);
                request_message.addReceiver(getAID("coordinator"));

                send(request_message);
            }
        }

        private class Listen extends OneShotBehaviour
        {
            ACLMessage response;

            public void action()
            {
                response = receive(MessageTemplate.MatchSender(getAID("coordinator")));
                
                if (response == null) {
                    response = new ACLMessage(ACLMessage.REFUSE);
                    return;
                }

                search = response.getContent();
            }

            public int onEnd()
            {
                return response.getPerformative();
            }
        }

        private class AttendFailure extends OneShotBehaviour
        {
            public void action()
            {
                System.err.printf("Agent %s has no work to do, resting 5 seconds\n", myAgent.getName());
                block(5000);
            }
        }

        private class Download extends OneShotBehaviour
        {

            // pages = numero de paginas, enlace_scrapeo_xxx = enlace para el producto segun la pagina,
            // productos_enlace_xxx = lista del precio de lo que ha encontrado separado por ;

            private int pages = 5;
            private String enlace_scrapeo_ali, enlace_scrapeo_gear, enlace_scrapeo_amazon;
            private String productos_enlace_ali = " ";
            private String productos_enlace_gear = " ";
            private String productos_enlace_amazon = " ";

            private aux aux = new aux();

            public void onStart()
            {
                System.out.println("Iniciando recoleccion de informacion...");
                
                this.enlace_scrapeo_ali     = String.format("https://es.aliexpress.com/wholesale?&SearchText=%s&page=", search);
                this.enlace_scrapeo_gear    = String.format("https://es.gearbest.com/%s-_gear/", search);
                this.enlace_scrapeo_amazon  = String.format("https://www.amazon.es/s/keywords=%s&ie=UTF8&page=", search);
                
            }

            public void action()
            {
                System.out.printf("Agent %s is now Downloading: %s\n", myAgent.getName(), search);

                for(int i = 1; i < pages; i++) {               
                    scraper_aliexpress(enlace_scrapeo_ali+i);
                    scraper_gearbest(enlace_scrapeo_gear+i+".html");
                    scraper_amazon(enlace_scrapeo_amazon+i);
                }

                block(4000);
            }

            public void scraper_amazon(String url)
            {
                if (aux.getStatusConnectionCode(url) == 200) {
                    
                    // Obtengo el HTML de la web en un objeto Document
                    Document document = aux.getHtmlDocument(url);
                    // Busco todas las entradas que estan dentro de: 
                    Elements lista_productos    = document.select("#s-results-list-atf");
                    Elements productos  = lista_productos.select("li");
                    // Paseo cada una de las entradas
                    
                    for(int i = 0; i < productos.size(); ++i){
                        Elements precio = productos.get(i).select("> div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > span:nth-child(2)");                     
                        Elements nombre = productos.get(i).select("div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > h2:nth-child(1)");

                        productos_enlace_amazon += nombre.text()+";";
                        productos_enlace_amazon += (precio.text() != "") ? precio.text() : "null";
                        productos_enlace_amazon += ";amazon";
                        productos_enlace_amazon +=  (i < productos.size()) ? " - " : "" ; 
                    }
                    
                        
                }else
                    System.out.println("El Status Code no es OK es: "+aux.getStatusConnectionCode(url));
            }
    
            public void scraper_gearbest(String url)
            {
                            
                if (aux.getStatusConnectionCode(url) == 200) {
                
                    // Obtengo el HTML de la web en un objeto Document
                    Document document = aux.getHtmlDocument(url);
                    
                    // Busco todas las entradas que estan dentro de: 
                    Elements entradas = document.select("div.gbGoodsItem_outBox");
                    // Paseo cada una de las entradas
                    for (int i = 0; i < entradas.size(); ++i) {
                        
                        Elements goods_title = entradas.get(i).getElementsByClass("gbGoodsItem_titleInfor");
                        Elements goods_price = entradas.get(i).getElementsByClass("price-loading gbGoodsItem_price js-currency js-asyncPrice");
                        
                        String precio = goods_price.get(0).attr("data-currency");
            
                        productos_enlace_gear += goods_title.get(0).getElementsByClass("gbGoodsItem_title  gbGoodsItem_titlex  ").attr("title")+";";
                        productos_enlace_gear += precio + ";";
                        productos_enlace_gear += "gearbest";
                        productos_enlace_gear += (i < entradas.size()) ? " - " : "";
                    }
                    
                }else
                    System.out.println("El Status Code no es OK es: "+ aux.getStatusConnectionCode(url));
            }
            
            public void scraper_aliexpress(String url)
            {
                
                    if (aux.getStatusConnectionCode(url) == 200) {
                    
                    Document document = aux.getHtmlDocument(url);
                    
                    Elements entradas = document.select("div.info");
                    Elements enlaces = document.select("a.picRind");
                    
                    for (int i = 0; i < entradas.size(); ++i) {

                        String precio = entradas.get(i).getElementsByClass("price price-m").text();
                        String titulo = enlaces.get(i).getElementsByClass("picCore pic-Core-v").attr("alt");

                        if(titulo == ""){
                            titulo = enlaces.get(i).getElementsByClass("picCore").attr("alt");
                        }

                        productos_enlace_ali += titulo+";";
                        productos_enlace_ali += precio + ";";
                        productos_enlace_ali += "aliexpress";
                        productos_enlace_ali += (i < entradas.size()) ? " - " : "";
        
                    }
                    
                }else
                    System.out.println("El Status Code no es OK es: "+aux.getStatusConnectionCode(url));
            }

            public int onEnd()
            {
                scrapped_content += productos_enlace_ali + ":" + productos_enlace_amazon + ":" + productos_enlace_gear;

                return 0;
            }
        }

        private class Save extends OneShotBehaviour
        {
            ACLMessage message;

            public void action()
            {
                message = new ACLMessage(ACLMessage.INFORM);
                message.addReceiver(getAID("DatabaseManager"));
                message.setContent(scrapped_content);

                System.out.printf("\n\nAgent %s is sending information regarding %s to database\n\n", myAgent.getName(), search);

                send(message);
            }

            public int onEnd()
            {
                scrapped_content = "";
                return 0;
            }
        }

        Scraping()
        {
            super();

            registerFirstState(new InformManager(), "PING");
            registerState(new Listen(), "LISTEN");
            registerState(new AttendFailure(), "FAIL");
            registerState(new Download(), "DOWNLOAD");
            registerState(new Save(), "SAVE");

            registerDefaultTransition("PING", "LISTEN");
            registerTransition("LISTEN", "FAIL", ACLMessage.REFUSE);
            registerTransition("LISTEN", "DOWNLOAD", ACLMessage.AGREE);
            registerDefaultTransition("FAIL", "PING");
            registerDefaultTransition("DOWNLOAD", "SAVE");
            registerDefaultTransition("SAVE", "DOWNLOAD");
        }
    }

    public void setup()
    {
        addBehaviour(new Scraping());
        
        System.out.printf("Downloader agent: %s is ready\n", getName());
    }
}
