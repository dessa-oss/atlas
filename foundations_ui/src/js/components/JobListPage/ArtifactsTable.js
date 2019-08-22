import React from 'react';
import ArtifactRow from './ArtifactRow';

class ArtifactsTable extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      artifacts: [
        {
          id: '1',
          name: 'temp.jpg',
          date: '2019-05-01',
          size: '450 MB',
          url: 'http://www.pdf995.com/samples/pdf.pdf',
        },
        {
          id: '2',
          name: 'text.txt',
          date: '2019-05-02',
          size: '450 MB',
          url: 'http://www.pdf995.com/samples/pdf.pdf',
        },
        {
          id: '3',
          name: 'temp.jpg',
          date: '2019-05-03',
          size: '450 MB',
          url: 'http://www.pdf995.com/samples/pdf.pdf',
        },
        {
          id: '4',
          name: 'text.txt',
          date: '2019-05-04',
          size: '450 MB',
          url: 'http://www.pdf995.com/samples/pdf.pdf',
        },
      ],
    };
  }

  render() {
    const { artifacts } = this.state;
    return (
      <div className="container-artifacts-table">
        <div className="table-artifacts-header">
          <p>Artifact Name</p>
        </div>
        <div className="table-artifacts-header last" />
        {artifacts.map((artifact) => {
          return <ArtifactRow key={artifact.id} artifact={artifact} />;
        })}
      </div>
    );
  }
}

export default ArtifactsTable;
