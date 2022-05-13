#include <stdio.h>
#include <mpi.h>

// Simple program with a client/server topology to run processes
// in parallel. The server process will execute a control path
// and the client processes will execute a common parallel path (thread).
//
// Typically in distributed systems, this would be written as two
// separate programs. (See TSAM)

#define NO_PROCESSES 3

int main(int argc, char *argv[])
{
    MPI_Status status;
    int my_id, ierr, num_procs;
    int server_id;
    int range[NO_PROCESSES];
    // argc = command line arguments
    // argv = an array of strings of character pointers that were passed on the command line
    ierr = MPI_Init(&argc, &argv);
    // address of argc and arg sent to init
    // allow to make changes to argc and argv

    server_id = 0;

    /* find out MY process ID, and how many processes were started. */
    // pointer to a local variable, updated by the COMM
    // pass the global communicator
    ierr = MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
    ierr = MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    if(my_id == 0)
       printf("Server id (rank) is: %d\n", my_id);
    else
       printf("Client id (rank) is: %d\n", my_id);

    // Prepare program data to send to clients. MPI_Send/MPI_Recv specify
    // the datatype which is used

    range[0] = 0;
    range[1] = 0xffff/NO_PROCESSES;


    // Determine if this process is the server (root) process
    // Could pick any number here, as long as it is a rank of one of the
    // processes.

    if(my_id == server_id)
    {
       for(int i = 1; i < NO_PROCESSES; i++)
       {
           range[0] = 1000 * (i - 1);
           range[1] = range[0] + 1000;
           // know location of information and the size. void * buf is a generic pointer
           // can pass a pointer to anything we want. Tells it where to get stuff out of memory
           // count is the number of some primitive element in the buffer. Specified by datatype
           // dest is the rank of the processor we want to transmit the buffer
           // the tag isa generic integer value for distinguishing messages
           // Communicator brings all processes to the picture for distributed computing
           MPI_Send(range, 2, MPI_INT, i, 0, MPI_COMM_WORLD);
           printf("Server: sent to client %d\n", i);
       }
    }
    else
    // Slave process, receive the array range to calculate, and send
    // it back to the server when finished.
    {
       // Need to call on destination process MPI_recv to pull into destination process
       // specify the buffer. The buffer points to memory where it wants to store the data it received
       // count is the same as in the send.
       // the source is the rank of the process you want to receive from
       // give tag to know which type of message
       // same communicator
       // the status is about the success or failure of operation
       // it is a pointer. When we want MPI to give us something back, we give it a structure it can fill
       // in values and access the new values
       MPI_Recv(range, NO_PROCESSES, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
       printf("Client id: %d Received: %d %d\n",my_id, range[0], range[1]);
    }

    MPI_Finalize();
}
~                                                                                                                                        
~                                                                                                                                        
~                                                                                                                                        
~              