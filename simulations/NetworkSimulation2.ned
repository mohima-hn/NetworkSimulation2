//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 
package networksimulation2.simulations;
import inet.networks.base.WiredNetworkBase;
import inet.node.inet.StandardHost;
import inet.node.ethernet.EthernetSwitch;
import inet.node.inet.Router;
import inet.visualizer.canvas.integrated.IntegratedCanvasVisualizer;
import inet.common.misc.ThruputMeteringChannel;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.StandardHost;
import inet.node.ospfv2.OspfRouter;
import inet.node.ethernet.Eth100M;
import inet.queueing.contract.IPacketBuffer;
//
// TODO auto-generated type
//
import inet.queueing.filter.RedDropper;
import inet.queueing.queue.CompoundPacketQueueBase;
import inet.queueing.queue.PacketQueue;
import ned.DatarateChannel;

module REDQueue extends CompoundPacketQueueBase
{
    submodules:
        red: RedDropper {
            wq = default(0.002);
            minth = default(30);
            maxth = default(90);
            maxp = default(0.10);
            pkrate = default(8333.333);
        }
        fifo: PacketQueue;
    connections:
        in --> red.in;
        red.out --> fifo.in;
        fifo.out --> out;
}
network NetworkSimulation2
{
    parameters:
//        @statistic[dropCount](source=count(drop); record=last,vector?);
//        @statistic[droppedPacketsQueueOverflow](title="dropped packets: queue overflow"; source=packetDropReasonIsQueueOverflow(packetDropped); record=count; unit=pk; interpolationmode=none);
        // the statistical value is the length of the packet that is dropped due to queue overflow
        //   	@statistic[queueBitLength](title="queue bit length"; source=warmup(atomic(constant0(packetPushEnded) + sum(packetLength(packetPushStarted)) - sum(packetLength(packetPulled)) - sum(packetLength(packetRemoved)) - sum(packetLength(packetDropped)))); record=last,max,timeavg,vector; unit=b; interpolationmode=sample-hold; autoWarmupFilter=false);
        //        // the statistical value is the queueing time of packets
        //    @statistic[removedPacketLengths](title="removed packet lengths"; source=packetLength(packetRemoved); record=sum,vector; unit=pk; interpolationmode=none);
        //        // the statistical value is the number of packets in the buffer
//        @statistic[outgoingPackets](source=count(drop); record=last,vector?);
//        @statistic[incomingPackets](source=count(drop); record=last,vector?);
        @display("bgb=806,406");

    types:
        channel C extends ThruputMeteringChannel
        {
            @statistic[utilization](source="timeavg(channelBusy)";record=last?);
//            @statistic[packets](source="constant1(messageSent)";record=count?;interpolationmode=none);
//            @statistic[busy](source=channelBusy;record=vector?;interpolationmode=sample-hold);
            datarate = 200000000 bps;
        }
    submodules:
        buffer: <default("")> like IPacketBuffer if typename != "" {
            parameters:
                @display("p=31.387499,170.1");
        }
        host1: StandardHost {
            parameters:
                @display("p=195.4125,158.9625");
            gates:
                pppg[1];
        }
        host2: StandardHost {
            parameters:
                @display("p=443.475,360.45");
            gates:
                pppg[1];
        }
        host3: StandardHost {
            parameters:
                @display("p=373.6125,50.625");
            gates:
                pppg[1];
        }
        host4: StandardHost {
            parameters:
                @display("p=586.2375,123.525");
            gates:
                pppg[1];
        }
        host5: StandardHost {
            parameters:
                @display("p=104.2875,320.9625");
            gates:
                pppg[1];
        }
        host6: StandardHost {
            parameters:
                @display("p=502.19998,198.45");
            gates:
                pppg[1];
        }
        host7: StandardHost {
            parameters:
                @display("p=736.0875,123.525");
            gates:
                pppg[1];
        }

        router5: OspfRouter {
            parameters:
                @display("p=105,233");
                hasStatus = true;
            gates:
                pppg[2];

        }
        router1: OspfRouter {
            parameters:
                @display("p=234.9,232.875");
                hasStatus = true;
            gates:
                pppg[4];

        }
        router3: OspfRouter {
            parameters:
                @display("p=373.6125,123.525");
                hasStatus = true;
            gates:
                pppg[5];

        }
        router2: OspfRouter {
            parameters:
                @display("p=373.6125,307.8");
                hasStatus = true;
            gates:
                pppg[5];

        }
        router6: OspfRouter {
            parameters:
                @display("p=434.3625,205.53749");
                hasStatus = true;
            gates:
                pppg[3];

        }
        router4: OspfRouter {
            parameters:
                @display("p=616.6125,205.53749");
                hasStatus = true;
            gates:
                pppg[4];
        }
        router7: OspfRouter {
            parameters:
                @display("p=736.0875,205.53749");
                hasStatus = true;
            gates:
                pppg[2];
        }


        configurator: Ipv4NetworkConfigurator {
            parameters:
                config = xml("<config>"+
        			"<interface among='host5 router5' address='192.168.1.x' netmask='255.255.255.0' />"+
                    "<interface among='host1 router1' address='192.168.2.x' netmask='255.255.255.0' />"+
                    "<interface among='host2 router2' address='192.168.3.x' netmask='255.255.255.0' />"+
                    "<interface among='host3 router3' address='192.168.4.x' netmask='255.255.255.0' />"+
                    "<interface among='host4 router4' address='192.168.5.x' netmask='255.255.255.0' />"+
                    "<interface among='host6 router6' address='192.168.6.x' netmask='255.255.255.0' />"+
                    "<interface among='host7 router7' address='192.168.7.x' netmask='255.255.255.0' />"+
                    "<interface among='router1 router5' address='192.168.60.x' netmask='255.255.255.0'/>"+
                    "<interface among='router1 router2' address='192.168.20.x' netmask='255.255.255.0'/>"+
                    "<interface among='router1 router3' address='192.168.10.x' netmask='255.255.255.0'/>"+
                    "<interface among='router3 router2' address='192.168.70.x' netmask='255.255.255.0'/>"+
                    "<interface among='router3 router6' address='192.168.80.x' netmask='255.255.255.0'/>"+
                    "<interface among='router6 router2' address='192.168.90.x' netmask='255.255.255.0'/>"+
                    "<interface among='router3 router4' address='192.168.50.x' netmask='255.255.255.0'/>"+
                    "<interface among='router4 router2' address='192.168.30.x' netmask='255.255.255.0'/>"+
                    "<interface among='router4 router7' address='192.168.40.x' netmask='255.255.255.0'/>"+
                    "<route hosts='host*' destination='*' netmask='0.0.0.0' interface='ppp0'/>"+
                    "</config>");
                addStaticRoutes = false;
                addDefaultRoutes = false;
                @display("p=61,58;is=s");
        }
    connections allowunconnected:
 		router2.pppg[0]  <--> C <--> router3.pppg[0];
		router2.pppg[1]  <--> C <--> router4.pppg[1];
		router2.pppg[2]  <--> C <--> router6.pppg[1];
		router2.pppg[3]  <--> C <--> router1.pppg[0];
		router2.pppg[4]  <--> C <--> host2.pppg[0];
		router1.pppg[1]  <--> C <--> router3.pppg[1];
		router1.pppg[2]  <--> C <--> router5.pppg[0];
		router1.pppg[3]  <--> C <--> host1.pppg[0];
		router3.pppg[2]  <--> C <--> router6.pppg[0];
		router3.pppg[3]  <--> C <--> router4.pppg[0];
		router3.pppg[4]  <--> C <--> host3.pppg[0];
		router4.pppg[2]  <--> C <--> router7.pppg[0];
		router4.pppg[3]  <--> C <--> host4.pppg[0];
		router7.pppg[1]  <--> C <--> host7.pppg[0];
		router6.pppg[2]  <--> C <--> host6.pppg[0];
		router5.pppg[1]  <--> C <--> host5.pppg[0];
}
